# Generated by Django 3.0.5 on 2023-02-23 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_user_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('upload', models.FileField(upload_to='songs/')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='song_uploader', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
