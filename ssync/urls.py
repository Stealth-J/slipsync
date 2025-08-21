from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = "home"),
    path('settings', settings, name = "settings"),
    path('convert-to-<str:platform>', convert, name = "convert"),
    path('edit_slip', edit_slip, name = "edit_slip"),
    path('sync', sync, name = "sync"),
    path('contact', contact, name = "contact"),
    path('help', help, name = "help"),
]