from django.urls import path, include, re_path
# from django.conf.urls import url
from .views import *

# urlpatterns = [
#     path('', views.index, name ='painting-app-index')
# ]

urlpatterns = [
    path('', not_connected_view, name='not_connected'),
    path('FullPainting', not_connected_view, name='not_connected'),
    path('connected/', connected_view, name='connected'),
    path('connected/FullPainting', connected_fullpainting, name='ConnectedFull'),
    path('connected/SelfPortrait', self_portrait, name='SelfPortrait'),
    path('connected/vsWorld', vs_world, name='vsWorld'),
    path('connected/change_color', change_color, name='change_color'),
    path('connected/about_project', about_project, name='about_project'),
    path('connected/about_me', about_me, name='about_me'),
    path('about_project', about_project, name='about_project'),
    path('about_me', about_me, name='about_me'),
    re_path(r"^oauth/", include("social_django.urls", namespace="social")),
]
