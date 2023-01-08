"""institute URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from intuition import views

admin.site.site_header = "Intuition Academy Admin"
admin.site.site_title = "Intuition Academy Teacher Portal"
admin.site.index_title = "Welcome to Intuition Academy Teacher Portal"

urlpatterns = [
    path('', views.home ,name='home'),
    path('login/', views.st_login ,name='st_login'),
    path('detail/', views.st_detail, name='st_detail'),
    path('student-List/', views.st_list, name='st_list'),
    path('edit-St-Detail/<id>/', views.edit_st_detail, name='edit_st_detail'),
    path('log/<id>/', views.logs, name='logs'),
    path('add-student/', views.add_student, name='add_student'),
    path('filtered_by_dd/',views.filtered_by_dd, name='filtered_by_dd'),
    path('filtered_by_completed/',views.filtered_by_completed, name='filtered_by_completed'),
    path('filtered_by_email/',views.filtered_by_email, name='filtered_by_email'),
    path('getcertificate/', views.certificate, name='certificate'),
    path('verify-certificate/', views.certid_filter, name='certificate_id_filter'),
    path('admin/', admin.site.urls),
]
