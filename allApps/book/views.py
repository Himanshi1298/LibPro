from asyncio.windows_events import NULL
import imp
from pickle import NONE
from sqlite3 import Date
from django.shortcuts import render, redirect
from .models import *
from . .userAccount.models import *
from .forms import *
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from . import forms
from django.conf import settings 
from django.contrib import messages
from django.core.mail import send_mail
from datetime import date, timedelta

@login_required(login_url='login')
def bookDetailPg(request, id, bookName):
    bk = book.objects.get(pk = id)
    user = request.user
    try:
        loan = bookLoanDetail.objects.get(book_id = id, user_id = user.id, return_status = 'pending')
    except bookLoanDetail.DoesNotExist:
        loan = NONE
        
    context = {
        'bk' : bk,
        'loan' : loan
    }
    return render(request, 'bookDetails.html', context)

def returnBookNotification(email, book):
    subject = 'You Have Successfully Returned ' + book.book_title
    message = f'You Have Successfully Returned {book.book_title} on { date.today }'
    email_from = settings.EMAIL_HOST_USER
    reciver_list = [email]
    send_mail(subject, message , email_from , reciver_list)


def bookCheckoutNotification(email, book):
    subject = 'You Have Successfully Checked Out' + book.book_title
    message = f'You Have Successfully Checked Out {book.book_title}'
    email_from = settings.EMAIL_HOST_USER
    reciver_list = [email]
    send_mail(subject, message , email_from , reciver_list)

@login_required(login_url='login')
def returnBook(request, id):
    user = request.user
    userUse = userProfiles.objects.get(user_id = user.id)
    quanBook = book.objects.get(id = id)
    loanUpdate = bookLoanDetail.objects.get(book_id = id, user_id = user.id, return_status = "pending")
    loanUpdate.return_status = "returned"
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    loanUpdate.return_date = str(d1)
    quanBook.book_quantity += 1
    userUse.books_issued -= 1
    loanUpdate.save()
    quanBook.save() 
    userUse.save()
    returnBookNotification(user.email, quanBook)
    return redirect('home')


@login_required(login_url='login')
def checkOut(request, id):
    user = request.user
    bookLoanObj = bookLoanDetail(user_id = user.id, book_id = id)
    etd = datetime.now() + timedelta(days=10)
    etdFormat = etd.strftime("%Y-%m-%d")
    bookLoanObj.estimated_return_date = str(etdFormat)
    bookLoanObj.save()
    userUse = userProfiles.objects.get(user_id = user.id)
    userUse.books_issued += 1
    quanBook = book.objects.get(id = id)
    quanBook.book_quantity -= 1
    userUse.save()
    quanBook.save()
    bookCheckoutNotification(user.email, bookLoanObj.book)

    return redirect('home')