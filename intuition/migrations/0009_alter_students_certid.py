# Generated by Django 3.2.9 on 2022-12-04 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intuition', '0008_students_certid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='certid',
            field=models.CharField(blank=True, default='0', max_length=255, null=True, verbose_name='Certificate ID'),
        ),
    ]
