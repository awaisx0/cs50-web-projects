from django.urls import path

from . import views

# app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_page, name="random"),
    path("create_entry", views.create_entry, name="create_entry"),
    path("search", views.search, name="search"),
    # entry page
    path("wiki/<str:title>", views.page, name="page"),
]
