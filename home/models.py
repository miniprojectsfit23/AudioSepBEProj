from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os

# Create your models here.


def create_path(instance, filename):
    if instance.user is None:
        return os.path.join(
            'uploaded_songs/Anonymous/',
            filename
        )
    else:
        print(os.path.join(
            'uploaded_songs',
            str(instance.user),
            filename
        ))
        return os.path.join(
            'uploaded_songs',
            str(instance.user),
            filename
        )


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=500)

    def delete(self, *args, **kwargs):
        self.profile_picture.delete()
        super(User, self).delete(*args, **kwargs)

    def __str__(self):
        return(self.username)


class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    # if null, means anonymous user uploaded it
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="song_uploader")
    upload = models.FileField(upload_to=create_path)
