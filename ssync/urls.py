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

    path('admin-tourneys', admin_tourneys, name = "admin_tourneys"),
    path('tourney-create', tourney_create, name = "tourney_create"),
    path('tourney-update', tourney_update, name = "tourney_update"),
    path('tourney-delete/<str:pk>', tourney_delete, name = "tourney_delete"),
    path('tourney-filter', tourney_filter, name = "tourney_filter"),
    path('admin-markets', admin_markets, name = "admin_markets"),
]