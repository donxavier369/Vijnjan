# Generated by Django 5.0.3 on 2024-03-22 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_date_of_birth_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150),
        ),
    ]
