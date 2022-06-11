from django.urls import path

from . import polls

urlpatterns = [
    path('', polls.index, name='index'),
]