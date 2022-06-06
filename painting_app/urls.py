from django.urls import path, include
from django.conf.urls import url
from .views import not_connected_view, connected_view

# urlpatterns = [
#     path('', views.index, name ='painting-app-index')
# ]

urlpatterns = [
    path('', not_connected_view, name='not_connected'),
    path('masterpiece/', connected_view, name='masterpiece'),
    url(r"^oauth/", include("social_django.urls", namespace="social")),
]
