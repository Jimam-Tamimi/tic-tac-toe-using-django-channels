from django.urls import path
from django.urls.conf import include
from .views import *

urlpatterns = [
    path('', home), 
    path('play/<str:code>/<str:username>/', play), 
]
