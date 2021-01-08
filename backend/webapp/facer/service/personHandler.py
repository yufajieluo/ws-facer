#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2019 WShuai, Inc.
# All Rights Reserved.

# @author: WShuai, WShuai, Inc.

from django.conf import settings
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

import os
import time
import uuid
import json
import numpy
import base64
from PIL import Image
from io import BytesIO
from ..models import Person
from ..common.commRsp import CommRsp
from ..common.commPaging import CommPaging
from ..common.commRecognize import CommRecognize

class PersonHandler(object):
    def __init__(self, request, logger):
        self.request = request
        self.logger = logger
        self.media_root_path = settings.MEDIA_ROOT
        self.wait_recognize_path = settings.WAIT_PATH
        self.rsp_handler = CommRsp()
        self.paginator = CommPaging()
        self.recognize_handler = CommRecognize(logger)
        return

    def page_person(self, current_page = 0):
        person_objects = Person.objects.all().order_by('id')
        person_nums = Person.objects.count()
        contents, pages = self.paginator.paging(person_objects, person_nums, current_page)
        persons = [model_to_dict(content) for content in contents]
        rsp_body = {'rsp_body': {'persons': persons, 'pages': pages}}
        rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
        return rsp

    def save_person(self, person_name, person_sex, person_idn, person_image_data):
        try:
            person_object = Person.objects.get(idn = person_idn)
            rsp = self.rsp_handler.generate_rsp_msg(29003, None)
        except ObjectDoesNotExist:
            face_encodes, image_file = self.get_face_encodes(person_idn, person_image_data)
            if face_encodes:
                face_encode = face_encodes[0].tolist()
                Person.objects.create(
                    name = person_name,
                    sex = person_sex,
                    idn = person_idn,
                    photo = os.path.join('media', image_file),
                    encode = json.dumps([float('{0:.8f}'.format(item)) for item in face_encode]),
                    acquire = u'已采集'
                )
            rsp = self.rsp_handler.generate_rsp_msg(200, None)
        except Exception as e:
            self.logger.error('save person {} {} {} Exception: {}'.format(person_name, person_sex, person_idn, e))
            rsp = self.rsp_handler.generate_rsp_msg(29999, None)

        return rsp

    def remove_person(self, person_id):
        try:
            print('person id is {}{}'.format(type(person_id), person_id))
            person_object = Person.objects.get(id = person_id)
            os.remove(os.path.join(self.media_root_path, os.path.basename(person_object.photo)))
            person_object.delete()
            rsp = self.rsp_handler.generate_rsp_msg(200, None)
        except ObjectDoesNotExist:
            rsp = self.rsp_handler.generate_rsp_msg(200, None)
        except Exception as e:
            self.logger.error('remove person {} Exception: {}'.format(person_idn, e))
            rsp = self.rsp_handler.generate_rsp_msg(29999, None)
        return rsp

    def get_face_encodes(self, person_idn, image_data):
        if not os.path.isdir(self.media_root_path):
            os.makedirs(self.media_root_path)
        
        image_format = image_data.split(',')[0].split(';')[0].split('/')[-1]
        image_base_data = base64.b64decode(image_data.split(',')[-1])
        image_local_file = os.path.join(self.media_root_path, '{0}-{1}.{2}'.format(person_idn, uuid.uuid4(), image_format))
        with open(image_local_file, 'wb') as file_handler:
            file_handler.write(image_base_data)

        image_temp_file = self.recognize_handler.get_face_img(image_local_file)
        face_encodes = self.recognize_handler.get_face_encode(image_temp_file)
        self.recognize_handler.clear(image_temp_file)

        return face_encodes, os.path.basename(image_local_file)

    def save_photo(self, person_id, image_data):
        try:
            person_object = Person.objects.get(id = person_id)
            face_encodes, image_file = self.get_face_encodes(person_object.idn, image_data)

            if face_encodes:

                if os.path.basename(person_object.photo).split('.')[0] != 'default':
                    os.remove(os.path.join(self.media_root_path, os.path.basename(person_object.photo)))

                face_encode = face_encodes[0].tolist()
                person_object.photo = os.path.join('media', image_file)
                person_object.encode = json.dumps([float('{0:.8f}'.format(item)) for item in face_encode])
                person_object.acquire = u'已采集'
                person_object.save()

                rsp_body = {'rsp_body': {'photo': os.path.join('media', image_file)}}
                rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
            else:
                self.logger.error('image no face.')
                rsp = self.rsp_handler.generate_rsp_msg(29999, None)
        except Exception as e:
            self.logger.error('save photo Exception: {0}'.format(e))
            rsp = self.rsp_handler.generate_rsp_msg(29999, None)
        return rsp

    def recognize_photo(self, image_data):
        begin_time = time.time()

        if not os.path.isdir(self.wait_recognize_path):
            os.makedirs(self.wait_recognize_path)
        
        image_format = image_data.split(',')[0].split(';')[0].split('/')[-1]
        image_base_data = base64.b64decode(image_data.split(',')[-1])
        image_local_file = os.path.join(self.wait_recognize_path, 'recog-{0}.{1}'.format(uuid.uuid4(), image_format))

        with open(image_local_file, 'wb') as file_handler:
            file_handler.write(image_base_data)

        image_temp_file = self.recognize_handler.get_face_img(image_local_file)
        face_encodes = self.recognize_handler.get_face_encode(image_temp_file)
        self.recognize_handler.clear(image_temp_file)

        if face_encodes:
            face_encode = face_encodes[0]
            person_objects = Person.objects.all()
            known_encodings = [
                numpy.array(json.loads(person_object.encode)) for person_object in person_objects
            ]
            result = self.recognize_handler.recognize(known_encodings, face_encode)
            try:
                match_person_object = person_objects[result.index(True)]
                rsp_body = {'rsp_body': model_to_dict(match_person_object, exclude = 'encode')}
                rsp = self.rsp_handler.generate_rsp_msg(200, rsp_body)
            except Exception as e:
                self.logger.error('face_recognition Exception: {0}'.format(e))
                rsp = self.rsp_handler.generate_rsp_msg(29001, None)
        else:
            rsp = self.rsp_handler.generate_rsp_msg(29001, None)
        self.logger.info('use time is {0}s'.format(time.time() - begin_time))
        return rsp
