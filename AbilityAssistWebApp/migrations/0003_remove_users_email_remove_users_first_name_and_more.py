# Generated by Django 5.0.4 on 2024-04-15 04:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AbilityAssistWebApp', '0002_users_volunteers_delete_userp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='email',
        ),
        migrations.RemoveField(
            model_name='users',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='users',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='users',
            name='password1',
        ),
        migrations.RemoveField(
            model_name='users',
            name='password2',
        ),
        migrations.AddField(
            model_name='users',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]