from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    path(r'', views.index, name = 'index'),
    path(r'person/', views.person, name = 'person'),
    path(r'photo/', views.photo, name = 'photo'),

    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
