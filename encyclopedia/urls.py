from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("random", views.random_page, name="random_page"),
]