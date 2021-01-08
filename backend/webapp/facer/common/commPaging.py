#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2019 WShuai, Inc.
# All Rights Reserved.

# @author: WShuai, WShuai, Inc.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CommPaging(object):

    def __init__(self):
        return

    def paging(self, objects, nums, current_page):
        paginator = Paginator(objects, 10)

        try:
            contents = paginator.page(current_page)
        except PageNotAnInteger:
            contents = paginator.page(1)
        except EmptyPage:
            contents = paginator.page(paginator.num_pages)

        pages = {
            'total_nums': nums,
            'total_pages': contents.paginator.num_pages,
            'current_page': contents.number,
            'next_page': contents.next_page_number() if contents.has_next() else None,
            'previous_page': contents.previous_page_number() if contents.has_previous() else None,
        }
        return contents, pages
