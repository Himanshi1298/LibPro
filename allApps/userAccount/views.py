from pickle import NONE
from unicodedata import category
from django.contrib import auth
from django.contrib.auth.forms import UsernameField
from django.forms.fields import ImageField
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 
from django.db.models import Q
import uuid
from . forms import *
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . .book.models import *
from datetime import date
from . .book.forms import *


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        euser  = User.objects.filter(email = email)
        new_token = str(uuid.uuid4())
        passMail(email, new_token)
        up = userProfiles.objects.filter(user = euser)
        up.auth_token = new_token
        return redirect('login')

    return render(request, 'forgotPass.html')

def passMail(email, new_token):
    subject = 'Reset Password'
    message = f'Hi, click the button to reset your your password http://127.0.0.1:8000/resetPassword/{new_token}'
    email_from = settings.EMAIL_HOST_USER
    reciver_list = [email]
    send_mail(subject, message , email_from ,reciver_list)


def resetPass(request, auth_token):
    if request.method == 'POST':
        newvar = request.POST.get('url')
        check_token = userProfiles.objects.filter(auth_token = newvar).first()
        if check_token:
            user = User.objects.filter(username = check_token).first()
            return render(request, 'changePass.html')
    
    return render(request, 'email_verification.html')

@login_required(login_url='login')
def home(request):
    user = request.user
    if user.is_superuser:
        messages.info(request, 'Please Login Through Admin Panel Or Create New General User')
        return redirect('login')

    brk = book.objects.all().order_by('book_publication_date')
    form = curdBookForm()
    context = {
        'book' : brk,
        'form' : form,
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def bookSearch(request):
    user = request.user
    if user.is_superuser:
        messages.info(request, 'Please Login Through Admin Panel Or Create New General User')
        return redirect('login')
    bookToSearch = request.GET['query']
    lookups = Q(book_title__icontains = bookToSearch) | Q(book_author__icontains = bookToSearch)
    bk = book.objects.filter(lookups)
    context = {
        'books' : bk,
    }
    return render(request, 'search.html', context)
        
def authenticate_email(email, auth_token):
    subject = 'Your accounts need to be verified'
    message = f'Hi, click the button to activate your account http://127.0.0.1:8000/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    reciver_list = [email]
    send_mail(subject, message , email_from ,reciver_list)


def verify(request, auth_token):
    if request.method == 'POST':
        newvar = request.POST.get('url')
        check_token = userProfiles.objects.filter(auth_token = newvar).first()
        if check_token:
            user = User.objects.filter(username = check_token).first()
            user.is_active = True
            user.save()
            return redirect('login')
    
    return render(request, 'email_verification.html')

def registerUser(request):
    form  = userProfileForm()
    form2 = extendedProfileForm()
    form3 = userLinksForm()
    if request.method == 'POST':
        form  = userProfileForm(request.POST)
        form2 = extendedProfileForm(request.POST)
        form3 = userLinksForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')

        if User.objects.filter(username = username):
            messages.info(request, 'Username Already Taken')

        elif User.objects.filter(email = email):
            messages.info(request, 'Email Already Taken')

        elif form.is_valid():
            save_form =  form.save()
            auth_token = str(uuid.uuid4())
            profile = extendedProfileForm().save(commit=False)
            links   = userLinksForm().save(commit=False)
            links.user = save_form   
            profile.user = save_form
            profile.auth_token = auth_token
            save_form.save()
            links.save()
            profile.save()
            authenticate_email(save_form.email, auth_token)
            messages.info(request, "Please Verify your Email.")
        else:
            messages.info(request, "Password must be atleast eight characters and shall contain one small, capital and a special character")

    context = {'form':form, 'form2':form2}
    return render(request, "registration.html", context)

def calculateFine(user):
    loanBook = bookLoanDetail.objects.all().filter(user_id = user.id)
    for loan in loanBook:
        d1 = loan.issue_date
        d2 = loan.return_date
        d3 = loan.estimated_return_date
        d4 = date.today()
        d5 = (d4 - d3)
        try:
            fineBook = bookFine.objects.get(loan_id = loan.id) 
        except:
            fineBook = None

        
        if d2 == None:
            if int(d5.days) > 0 and fineBook == None:
                fn = bookFine(loan_id = loan.id, fine = 5, user_id = user.id)
                fn.save()

        elif d2 != None and fineBook == None:
            d6 = d2 - d1
            if int(d6.days) > 10:
                fn = bookFine(loan_id = loan.id, fine = 5, user_id = user.id)
                fn.save()


def loginUser(request):
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # userProfile = userProfiles.objects.filter(user = user.id).first()
        if user is not None:
            if user.is_superuser:
                messages.info(request, 'Please Login Through Admin Panel Or Create New General User')
            elif user.is_active:
                calculateFine(user)
                login(request, user)
                return redirect('home')     
            else:
                messages.info(request, 'Please Verify Your Account')
    
        else:
            messages.info(request, 'Username or Password Is Incorrect')

    return render(request, 'login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='login')
@login_required(login_url='login')
def profilePg(request, st):
    user = request.user
    if user.is_superuser:
        messages.info(request, 'Please Login Through Admin Panel Or Create New General User')
        return redirect('login')

    pgUser      = User.objects.get(pk = request.user.id)
    profileUser = userProfiles.objects.get(user = pgUser)
    userLink    = userlinks.objects.get(user = pgUser)
    form  = userProfileForm(instance=pgUser)
    form2 = extendedProfileForm(instance = profileUser)
    form3 = userLinksForm(instance = userLink)
    if  request.method == 'POST':
        formName  = request.POST.get('profile-form')
        form2Name = request.POST.get('link-form')
        if formName == 'profile-form':
            pgUser.first_name               = request.POST.get('first_name')
            profileUser.bio                 = request.POST.get('bio')
            profileUser.address             = request.POST.get('address')
            image                           = request.FILES.get('user_profile_image')
        
            if image:
                profileUser.user_profile_image  = request.FILES.get('user_profile_image')
                # print(profileUser.user_profile_image)
            pgUser.save()
            profileUser.save()
            return redirect('profile', 'all')

        if form2Name == 'link-form':
            userLink.user    = request.user     
            userLink.website = request.POST.get('website')
            userLink.github  = request.POST.get('github')
            userLink.twitter = request.POST.get('twitter')
            userLink.linkdin = request.POST.get('linkdin')
            userLink.save()
            return redirect('profile', 'all')

    postImg = userProfiles.objects.all()
    fineBook = bookFine.objects.all().filter(user_id = user.id)
    user = request.user
    profileBook = bookLoanDetail.objects.all().filter(user_id = user.id)
    bk = book.objects.all()
    
    context = {
        'postImg'     : postImg,
        'profileBook' : profileBook,
        'fineBook'    : fineBook,
        'bk'          : bk,
        'st'          : st,
        'form'        : form,
        'form2'       : form2,
        'form3'       : form3,
    }
    return render(request, 'profile.html', context)

    