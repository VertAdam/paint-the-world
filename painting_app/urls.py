from django.urls import path, include
from django.conf.urls import url
from .views import *

# urlpatterns = [
#     path('', views.index, name ='painting-app-index')
# ]

urlpatterns = [
    path('', not_connected_view, name='not_connected'),
    path('connected/', connected_view, name='connected'),
    path('connected/FullPainting', connected_fullpainting, name='ConnectedFull'),
    path('connected/SelfPortrait', self_portrait, name='SelfPortrait'),
    path('connected/vsWorld', vs_world, name='vsWorld'),
    url(r"^oauth/", include("social_django.urls", namespace="social")),
]
