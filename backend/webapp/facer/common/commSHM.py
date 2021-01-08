#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2019 WShuai, Inc.
# All Rights Reserved.

# @author: WShuai, WShuai, Inc.

class SHMHandler(object):
    def __init__(self):
        self.shm = {
            'shm_encodes': [],
            'shm_persons': []
        }
        return

    def sync(self, shm_persons, shm_encodes):
        self.shm['shm_persons'] = shm_persons
        self.shm['shm_encodes'] = shm_encodes
        return

    def update(self, person, encode):
        try:
            index = self.shm['shm_persons'].index(person)
            self.shm['shm_encodes'][index] = encode
        except:
            self.shm['shm_persons'].append(person)
            self.shm['shm_encodes'].append(encode)
        return

    def gets(self):
        return self.shm['shm_persons'], self.shm['shm_encodes']

    def get_encodes(self):
        return self.shm['shm_encodes']

    def get_person(self, index):
        return self.shm['shm_persons'][index]

    def remove(self, person):
        try:
            index = self.shm['shm_persons'].index(person)
            self.shm['shm_persons'].pop(index)
            self.shm['shm_encodes'].pop(index)
        except:
            pass
        return

SHM = SHMHandler()
