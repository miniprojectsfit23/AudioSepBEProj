from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = "home"
urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("account/", views.profile, name="profile"),
    path("song/<str:url>/", views.song, name="song"),
    path("delete-song/<str:url>/", views.delete_song, name="delete-song"),
    path("edit-song/<str:url>/", views.edit_song, name="edit-song"),
    path("change-password/",
         views.change_password, name="change-password"),
    path("delete-account/",
         views.delete_account, name="delete-account"),
]
urlpatterns += staticfiles_urlpatterns()
