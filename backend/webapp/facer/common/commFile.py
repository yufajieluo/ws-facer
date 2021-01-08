#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2019 WShuai, Inc.
# All Rights Reserved.

# @File: commFile.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2019/10/26 12:10

import os
import hashlib

class CommFile(object):
    def __init__(self):
        #self.logger = logger
        return

    def download(self, source_file, target_file):
        with open(target_file, 'wb+') as destination:
            for chunk in source_file.chunks():
                destination.write(chunk)
        return

    def compute_md5(self, target_file):
        if not os.path.isfile(target_file):
            return
        hash_md5 = hashlib.md5()
        file_object = open(target_file, 'rb')
        while True:
            content = file_object.read(8096)
            if not content:
                break
            hash_md5.update(content)
        file_object.close()
        return hash_md5.hexdigest()