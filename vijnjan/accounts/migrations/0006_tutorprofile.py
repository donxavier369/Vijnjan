# Generated by Django 5.0.3 on 2024-03-25 14:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.CharField(default='', max_length=100)),
                ('certificate', models.FileField(upload_to='tutorprofile/pdf')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
