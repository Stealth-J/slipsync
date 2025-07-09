from django.urls import path
from .views import *

urlpatterms = [
    path('', home, name = "home")
]