from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

import json
import logging
from .service import personHandler

logger = logging.getLogger('facer')

def index(request):
    context = {'echo': 'hello'}
    return HttpResponse(json.dumps(context), content_type = 'application/json')

def person(request):
    context = {}
    person_handler = personHandler.PersonHandler(request, logger)
    if request.method == 'GET':
        context = person_handler.page_person(current_page = int(request.GET.get('page')))
    elif request.method == 'POST':
        request_post = json.loads(request.body)
        context = person_handler.save_person(
            request_post.get('name'),
            request_post.get('sex'),
            request_post.get('idn'),
            request_post.get('image_data')
        )
    elif request.method == 'DELETE':
        request_delete = json.loads(request.body)
        context = person_handler.remove_person(request_delete.get('person_id'))
    return HttpResponse(json.dumps(context), content_type="application/json")

def photo(request):
    context = {}
    person_handler = personHandler.PersonHandler(request, logger)
    if request.method == 'PUT':
        request_post = json.loads(request.body)
        context = person_handler.recognize_photo(request_post.get('image_data'))
    elif request.method == 'POST':
        request_post = json.loads(request.body)
        context = person_handler.save_photo(request_post.get('person_id'), request_post.get('image_data'))
    return HttpResponse(json.dumps(context), content_type="application/json")
