#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2019 WShuai, Inc.
# All Rights Reserved.

# @author: WShuai, WShuai, Inc.

from django.conf import settings

import os
import uuid
import face_recognition
from PIL import Image

class CommRecognize(object):
    def __init__(self, logger):
        self.logger = logger
        self.temp_path = settings.TEMP_PATH
        self.tolerance = 0.4
        return

    def get_face_img(self, source_img):
        source_img_data = face_recognition.load_image_file(source_img)
        face_locations = face_recognition.face_locations(source_img_data)
        if face_locations:
            top, right, bottom, left = face_locations[0]
            face_image = source_img_data[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            target_img = os.path.join(self.temp_path, '{0}.jpg'.format(uuid.uuid4()))
            pil_image.save(target_img)
        else:
            target_img = None
        return target_img

    def get_face_encode(self, image_file):
        image_encode = []
        if image_file:
            image_data = face_recognition.load_image_file(image_file)
            image_encode = face_recognition.face_encodings(image_data)
        return image_encode

    def recognize(self, known_encodings, wait_encoding):
        return face_recognition.compare_faces(known_encodings, wait_encoding, tolerance = self.tolerance)

    def clear(self, temp_file):
        if temp_file:
            if os.path.isfile(temp_file):
                os.remove(temp_file)
        return
