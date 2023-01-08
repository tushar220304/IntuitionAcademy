from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.exceptions import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, auth
from django.db import models
from .models import *
from django.db.models import Q
from django.contrib.sessions.backends.db import SessionStore
import datetime
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def passGen(full_name): # Generates password for students
# 	name = full_name.split(' ')
# 	password = name[0][:3] + name[1][:3] + '@IA'
# 	return password

def home(request):
	if(request.method == 'POST') :
		name = request.POST['name']
		mail = request.POST['mail']
		message = request.POST['message']
		send_mail(
			f'HI {name}',
			f'Welcome in Intuition Academy - Intention to learn \nWe have recieved your contact request and We will contact you soon { name }.',
			settings.EMAIL_HOST_USER,
			[mail]
			)
		send_mail(
			f'Contact request',
			f'You recieved a new request from \n Name - {name} \n Email - {mail} \n Message - {message} ',
			settings.EMAIL_HOST_USER,
			['movie220304@gmail.com','pradeep1j97@gmail.com']
			)
		return render(request, 'intuition/intuitionAcademy.html', {'name':name})
	else:
		return render(request, 'intuition/intuitionAcademy.html')

def st_login(request):
	if (request.method == 'POST'):
		email = request.POST['mail']
		request.session['mail'] = email
		return redirect('st_detail')
	else :
		return render(request, 'intuition/st-login-page.html')

def st_detail(request):
	try:
		email = request.session['mail']
		detail = Students.objects.get(Email=email)
	except ObjectDoesNotExist:
		return HttpResponse(f"No data found related to this {email} mail id, please check your email and retry it.")
	return render(request, 'intuition/student_detail.html', {'detail':detail})

def edit_st_detail(request, id): # for teachers
	detail = Students.objects.get(id=id)
	if 'update' in request.POST:
	    feePaid = int(request.POST['feesPaid'])
	    detail.Fees_Paid += int(request.POST['feesPaid'])
	    detail.Fees_left = detail.Total_Fees - detail.Fees_Paid
	    detail.Fees_Counter += 1
	    detail.DD = detail.DOJ + relativedelta(months=detail.Fees_Counter)
	    if (detail.Fees_left == 0 and detail.Fees_Paid == detail.Total_Fees) :
	        detail.Status = 'completed'
	        detail.DD = detail.DOJ
	    detail.save()
	    stLog = Log(Name_id=detail.id,PaidAmt=feePaid)
	    stLog.save()
	    msg_plain = render_to_string('intuition/st_detail_email.txt')
	    msg_html = render_to_string('intuition/st_update_detail_email.html', {'detail': detail})
	    send_mail(
				f'Fee Updation',msg_plain,settings.EMAIL_HOST_USER,[detail.Email],html_message=msg_html,)
	    return redirect('st_list')
	elif 'leave' in request.POST:
		detail.Status = 'leave'
		detail.save()
		send_mail(
			f'Sorry to see you goo',
			f'Intuition Academy - Intention to learn \n We regret to see you go so please give us your valuable feed back by replying to this mail.',
			settings.EMAIL_HOST_USER,
			[detail.Email]
			)
		return redirect('st_list')
	else :
		return render(request, 'intuition/edit-st-detail.html', {'detail':detail})

def add_student(request): # for teachers
	course = Course_Name.objects.all()
	if (request.method == 'POST'):
		Full_Name = request.POST['full_name']
		Email = request.POST['email']
# 		password = passGen(Full_Name)
		Course = request.POST['course_list']
		DOJ = datetime.date.today()
		Duration = request.POST['duration']
		TotalFees = int(Duration) * int(Course_Name.objects.values_list('Fees_per_month', flat=True).get(id=Course))
		Feesleft = TotalFees
		dol = DOJ + relativedelta(months=int(Duration))
		dd = DOJ + relativedelta(months=1)
		CourseName = Course_Name.objects.values_list('Name', flat=True).get(id=Course)
		student = Students(Full_Name=Full_Name,Email=Email,Course_id=Course,DOL=dol,DD=dd,Duration=Duration,Total_Fees=TotalFees,Fees_left=Feesleft)
		student.save()
		detail = Students.objects.get(Email=Email)
		msg_plain = render_to_string('intuition/st_detail_email.txt')
		msg_html = render_to_string('intuition/st_detail_email.html', {'detail': detail})
		send_mail(
			f'Hi {Full_Name}',
			f'Welcome in Intuition Academy - Intention to learn \n Your Details are given below :- \n Name - {Full_Name} \n Email - {Email} \n Date of Joining - {DOJ} \n Enrolled Course - {CourseName} \n Duration - {Duration} months \n Total Fees - {TotalFees}',
			settings.EMAIL_HOST_USER,
			[Email]
			)
    #     send_mail(
				# f'Fee Updation',
				# msg_plain,
				# settings.EMAIL_HOST_USER,
				# [detail.Email],
				# html_message=msg_html,
				# )
		return redirect('home')
	else :
		return render(request, 'intuition/add-new-student.html', {'course_list':course})

def st_list(request): # for teachers
	if (request.method == 'POST'):
		eid = request.POST['email']
		request.session['email'] = eid
		return redirect(filtered_by_email)
	else :
		detail_st = Students.objects.filter(Status='pursuing').order_by('-DOJ')
		paginator = Paginator(detail_st, 8)
		page = request.GET.get('page')
		try:
			detail = paginator.page(page)
		except PageNotAnInteger:
			detail = paginator.page(1)
		except EmptyPage:
	 		detail = paginator.page(paginator.num_pages)
		return render(request, 'intuition/student-names.html', {'detail':detail})

def filtered_by_email(request): # for teachers
	try:
		eid = request.session['email']
		detail = Students.objects.get(Email=eid)
		if (request.method == 'POST'):
			detail.Fees_Paid += int(request.POST['feesPaid'])
			detail.Fees_left = detail.Total_Fees - detail.Fees_Paid
			detail.Fees_Counter += 1
			detail.DD = detail.DOJ + relativedelta(months=detail.Fees_Counter)
			if (detail.Fees_left == 0 and detail.Fees_Paid == detail.Total_Fees) :
				detail.Status = 'completed'
			detail.save()
			CourseName = detail.Course.Name
			send_mail(
				f'Fees Updation',
				f'Welcome in Intuition Academy - Intention to learn \n Your Details are given below :- \n Name - {detail.Full_Name} \n Email - {detail.Email} \n Date of Joining - {detail.DOJ} \n Enrolled Course - {CourseName} \n Duration - {detail.Duration} months \n Fees left = Total Fees - Fees Paid \n Fees left = {detail.Total_Fees} - {detail.Fees_Paid} = {detail.Fees_left}',
				settings.EMAIL_HOST_USER,
				[detail.Email]
				)
			return redirect('st_list')
		else :
			return render(request, 'intuition/edit-st-detail.html', {'detail':detail})
	except ObjectDoesNotExist:
		return HttpResponse(f"No record found related to this {eid} mail id.")

def filtered_by_dd(request): # for teachers
	now = timezone.now()
	detail_st = Students.objects.filter(Status='pursuing').filter(DD__gte=now).order_by('DD')
	paginator = Paginator(detail_st, 8)
	page = request.GET.get('page')
	try:
		detail = paginator.page(page)
	except PageNotAnInteger:
		detail = paginator.page(1)
	except EmptyPage:
		detail = paginator.page(paginator.num_pages)
	return render(request, 'intuition/student-names.html', {'detail':detail})

def filtered_by_completed(request): # for teachers
	detail_st = Students.objects.filter(Status='completed')
	paginator = Paginator(detail_st, 10)
	page = request.GET.get('page')
	try:
		detail = paginator.page(page)
	except PageNotAnInteger:
		detail = paginator.page(1)
	except EmptyPage:
		detail = paginator.page(paginator.num_pages)
	return render(request, 'intuition/student-names.html', {'detail':detail})


def logs(request, id):
	name = Students.objects.get(id=id)
	log = Log.objects.filter(Name=id).order_by('-DateOfPayment')
	return render(request, 'intuition/st-log.html', {'log':log, 'name':name})


def certificate(request):
	return render(request, 'intuition/certificate.html')

def certid_filter(request):
    st_certid = request.GET.get('certid', None)
    try :
        student = Students.objects.get(certid=st_certid, Status = 'completed')
    except:
        student = None
    if st_certid is None:
        return render(request, 'intuition/verify_cert.html')
    if student:
        return render(request, 'intuition/student_detail.html', {'detail':student})
    else:
	    return HttpResponse(f'Sorry! This Certificate ID <b>{st_certid}</b> is not valid or not approved by government.')