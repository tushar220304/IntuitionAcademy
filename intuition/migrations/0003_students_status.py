# Generated by Django 3.2.9 on 2021-11-15 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intuition', '0002_students_fees_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='Status',
            field=models.CharField(choices=[('pursuing', 'PURSUING'), ('completed', 'COMPLETED'), ('leave', 'LEAVE')], default='pursuing', max_length=15),
        ),
    ]
