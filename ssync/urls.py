from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = "home"),
    path('settings', settings, name = "settings"),
    path('convert-to-<str:slip>', convert, name = "convert"),
    path('contact', contact, name = "contact"),
]