from django.urls import path

from . import views

# app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_page, name="random"),
    path("<str:title>", views.page, name="page"),
]
