from pickle import FALSE, NONE
from turtle import bk
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . .book.models import *
from . .book.forms import *
from . .userAccount.models import *
from . .userAccount.forms import *

# Create your views here.
def customAdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            isAdmin = user.is_superuser
            if isAdmin:
                login(request, user)
                return redirect('adminHome')     
            else:
                messages.warning(request, 'You are not authorized for the Admin Login')
    
        else:
            messages.info(request, 'Username or Password Is Incorrect')

    return render(request, 'adminLogin.html')

@login_required(login_url='adminLogin')
def logoutUser(request):
    logout(request)
    return redirect('adminLogin')

@login_required(login_url='adminLogin')
def adminHome(request):
    user = request.user
    isAdmin = user.is_superuser
    if isAdmin:
        return render(request, 'adminHome.html')
    else:
        return redirect('login')

@login_required(login_url='adminLogin')
def userSearch(request, appName, appModule):
    userToSearch = request.GET['query']
    us = User.objects.filter(username__icontains = userToSearch, is_superuser = False)
    context = {
        'us' : us,
        'appName' : appName,
        'appModule' : appModule,
    }
    return render(request, 'searchUser.html', context)
            

@login_required(login_url='adminLogin')
def addModel(request, appName, appModule):
    if appModule == 'bookCategories':
        bookForm = curdBookCategories()
    else:
        bookForm = curdBookForm()

    context = {
        'bookForm' : bookForm,
        'appModule' : appModule,
    }
    return render(request, 'addModel.html', context)


@login_required(login_url='adminLogin')
def listDisplay(request, appName, appModule):
    user = request.user
    isAdmin = user.is_superuser
    if isAdmin:
        if appName == 'book':
            allBook = book.objects.all()
            loanDetail = bookLoanDetail.objects.all()
            bookCat = bookCategory.objects.all()
            bookFinePayment = bookFinePayDetail.objects.all()
            bkFine = bookFine.objects.all()
            context = {
                    'allBook'             : allBook,
                    'loanDetail'          : loanDetail,
                    'bookCat'             : bookCat,
                    'bkFine'              : bkFine,
                    'bookFinePayment'     : bookFinePayment,
                    'appName'             : appName,
                    'appModule'           : appModule
            }
            return render(request, 'bookDet.html', context)
        else:
            allUser = User.objects.all().filter(is_superuser = False)
            userProf = userProfiles.objects.all()
            context = {
                'allUser'   : allUser,
                'userProf'  : userProf,
                'appName'   : appName,
                'appModule' : appModule
            }
            return render(request, 'adminHome.html', context)
    
    else:
        messages.warning(request, "Please Login at User Portal")
        return redirect('login')


@login_required(login_url='adminlogin')
def userFormAll(request, id, st):
    user = request.user
    isAdmin = user.is_superuser
    if isAdmin:    
        userProf = userProfiles.objects.get(user_id = id)
        userLinkProf = userlinks.objects.get(user_id = id)
        upForm = extendedProfileForm(instance=userProf)
        ulForm = userLinksForm(instance=userLinkProf)
        foamUser = User.objects.get(pk = userProf.user_id)
        try:
            loanBook = bookLoanDetail.objects.all().filter(user_id = id)
        except bookLoanDetail.DoesNotExist:
            loanBook = NONE

        bk = book.objects.all()
        print(loanBook)

        print(book)
        context = {
            'foamUser'     : foamUser, 
            'upForm'       : upForm,
            'ulForm'       : ulForm,
            'loanBook'     : loanBook,
            'bk'           : bk,
            'st'           : st,
        } 

        if request.method == 'POST':    
            formOne  = request.POST.get('profile-form')
            formTwo = request.POST.get('link-form')
            if formOne == 'profile-form':
                foamUser.first_name          = request.POST.get('first.name')
                userProf.phone               = request.POST.get('phone')
                userProf.bio                 = request.POST.get('bio')
                userProf.address             = request.POST.get('address')
                image                        = request.FILES.get('user_profile_image')
                if image:
                    userProf.user_profile_image  = request.FILES.get('user_profile_image')

                userProf.save()
                return redirect('userFormAll', id)

            if formTwo == 'link-form':
                userLinkProf.website = request.POST.get('website')
                userLinkProf.github  = request.POST.get('github')
                userLinkProf.twitter = request.POST.get('twitter')
                userLinkProf.linkdin = request.POST.get('linkdin')
                userLinkProf.save()
                return redirect('userFormAll', id)
      
    return render(request, 'renderForm.html', context)