from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = "home"
urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("song/<str:url>/", views.song, name="song"),
    path("delete_song/<str:url>/", views.delete_song, name="delete_song"),
]
urlpatterns += staticfiles_urlpatterns()
