# Generated by Django 3.2.9 on 2021-11-19 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intuition', '0004_course_name_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='password',
        ),
    ]
