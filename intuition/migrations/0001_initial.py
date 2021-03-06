# Generated by Django 3.2.9 on 2021-11-09 10:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course_Name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=1000)),
                ('Fees_per_month', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Courses',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Full_Name', models.CharField(max_length=1000, verbose_name='Full Name')),
                ('Email', models.EmailField(max_length=600, unique=True, verbose_name='Email Address')),
                ('password', models.CharField(blank=True, max_length=1000, verbose_name='Password')),
                ('DOJ', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of Joining')),
                ('DOL', models.DateTimeField(blank=True, verbose_name='Course Ending Date')),
                ('DD', models.DateTimeField(blank=True, verbose_name='Next Due Date')),
                ('Duration', models.IntegerField()),
                ('Total_Fees', models.IntegerField()),
                ('Fees_Paid', models.IntegerField(default=0)),
                ('Fees_left', models.IntegerField(default=0)),
                ('Course', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='intuition.course_name')),
            ],
            options={
                'verbose_name': 'Students',
                'verbose_name_plural': 'Students',
            },
        ),
    ]
