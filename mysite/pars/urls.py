from django.urls import path

from .views import *

urlpatterns = [
    path('', Coins, name="load_info"),
]
