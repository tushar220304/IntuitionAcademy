from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce import models as tinymce_models

Status = (
    ('pursuing','PURSUING'),
    ('completed', 'COMPLETED'),
    ('leave', 'LEAVE'),
)

class Course_Name(models.Model):
	Name = models.CharField(max_length=1000)
	Fees_per_month = models.IntegerField()
	Description = tinymce_models.HTMLField()

	class Meta:
		verbose_name = ("Courses")
		verbose_name_plural = ("Courses")

	def __str__(self):
		return self.Name


class Students(models.Model):
	Full_Name = models.CharField(verbose_name='Full Name', max_length=1000)
	Status = models.CharField(max_length=15, choices=Status, default='pursuing')
	Email = models.EmailField(verbose_name='Email Address', max_length=600, unique=True)
	password = models.CharField(verbose_name='Password', max_length=1000, blank=True)
	Course = models.ForeignKey(Course_Name, default=1, on_delete=models.SET_DEFAULT, blank=True)
	DOJ = models.DateTimeField(verbose_name='Date of Joining', default=timezone.now)
	DOL = models.DateTimeField(verbose_name='Course Ending Date', blank=True)
	DD = models.DateTimeField(verbose_name='Next Due Date', blank=True)
	Duration = models.IntegerField()
	Total_Fees = models.IntegerField()
	Fees_Paid = models.IntegerField(default=0)
	Fees_left = models.IntegerField(default=0)
	Fees_Counter = models.IntegerField(default=0)

	class Meta:
		verbose_name = ("Students")
		verbose_name_plural = ("Students")


	def __str__(self):
		return self.Full_Name