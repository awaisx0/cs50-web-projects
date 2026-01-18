from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.create_new_listing, name="new_listing"),
    path("listings/<int:listing_id>", views.listing_view, name="listing_view"),
    path("bid/<int:listing_id>", views.bid_view, name="bid_view"),
    path("comment/<int:listing_id>", views.comment_view, name="comment_view")
]
