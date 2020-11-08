from django.urls import path
from django.views.static import serve

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<username>", views.ProfileView.as_view(), name="profile"),
    path("following", views.Following.as_view(), name="following"),

    # API routes
    path("profile/<int:user_id>/follow", views.follow, name="follow"),
    path("update_post/<int:post_id>", views.update_post, name="update_post"),
]
