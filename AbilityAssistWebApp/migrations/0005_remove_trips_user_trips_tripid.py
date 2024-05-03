# Generated by Django 5.0.4 on 2024-04-21 14:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AbilityAssistWebApp', '0004_profile_remove_users_user_delete_volunteers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trips',
            name='user',
        ),
        migrations.AddField(
            model_name='trips',
            name='tripID',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
