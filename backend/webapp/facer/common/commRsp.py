#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2019 WShuai, Inc.
# All Rights Reserved.

# @File: commRsp.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2019/10/18 15:37

class CommRsp(object):
    def __init__(self):
        self.rsp_info = {
            # system
            200: u'成功',
            302: u'未登录',
            29999: u'系统错误',
            29001: u'系统中没有匹配到',
            29002: u'请确保镜头中有且只有一位人员头像',
            29003: u'身份证号已存在',
            29101: u'有未完成的批量任务，请稍后提交',
            29102: u'上传文件格式不正确',
            29103: u'上传文件为空',
            29104: u'文件校验失败',
        }
        return

    def generate_rsp_msg(self, rsp_code, rsp_body):
        try:
            rsp_info = self.rsp_info[rsp_code]
        except:
            rsp_info = 'failed'
        rsp_head = {
            'rsp_head': {
                'rsp_code': rsp_code,
                'rsp_info': rsp_info,
            }
        }
        if not rsp_body:
            return rsp_head
        else:
            return dict(**rsp_head, **rsp_body)
