from asyncio.windows_events import NULL
from email import message
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
    user = request.user
    if user.is_superuser:
        messages.info(request, "Please Create General User Profile")
        return redirect('login')
        
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
    message = f'You Have Successfully Returned' +  str(book.book_title) + ' on ' + str(date.today) 
    email_from = settings.EMAIL_HOST_USER
    reciver_list = [email]
    send_mail(subject, message , email_from , reciver_list)


def bookCheckoutNotification(email, book):
    etd = datetime.now() + timedelta(days=10)
    etdFormat = etd.strftime("%Y-%m-%d")
    subject = 'You Have Successfully Checked Out ' + book.book_title
    message = f'You Have Successfully Checked Out ' + book.book_title + ', the estimated return date is' + etdFormat
    email_from = settings.EMAIL_HOST_USER
    reciver_list = [email]
    send_mail(subject, message , email_from , reciver_list)

@login_required(login_url='login')
def returnBook(request, id):
    user = request.user
    if user.is_superuser:
        return redirect('adminLogin')

    userUse = userProfiles.objects.get(user_id = user.id)
    quanBook = book.objects.get(id = id)
    loanUpdate = bookLoanDetail.objects.get(book_id = id, user_id = user.id, return_status = "pending")
    if loanUpdate.return_status == 'pending':
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
        messages.info(request, "Book Returned Successfully")
        return redirect('profile', 'all')
    
    messages.info(request, "The book cannot be returned")
    return redirect('profile', 'all')

@login_required(login_url='login')

@login_required(login_url='login')
def checkOut(request, id):
    user = request.user
    if user.is_superuser:
        return redirect('adminLogin')

    try:
        bookLoanObj = bookLoanDetail(user_id = user.id, book_id = id)
    except:
        bookLoanObj = NONE

    userUse = userProfiles.objects.get(user_id = user.id)
    quanBook = book.objects.get(id = id)

    if bookLoanObj is not None:
        if bookLoanObj.return_status == 'pending':
            messages.info(request, 'You already have this book. You can re-new the book')
            return redirect('profile', 'all')
            
        else:
            if quanBook.book_quantity > 0 and userUse.books_issued < 5:
                etd = datetime.now() + timedelta(days=10) 
                etdFormat = etd.strftime("%Y-%m-%d")
                bookLoanObj.estimated_return_date = str(etdFormat)
                bookLoanObj.save() 
                userUse.books_issued += 1
                quanBook.book_quantity -= 1
                userUse.save()
                quanBook.save()
                bookCheckoutNotification(user.email, bookLoanObj.book)    
                messages.info(request, "Book Successfully Issued")
                return redirect('profile', 'all') 

    if quanBook.book_quantity > 0 and userUse.books_issued < 5:
        etd = datetime.now() + timedelta(days=10) 
        etdFormat = etd.strftime("%Y-%m-%d")
        bookLoanObj.estimated_return_date = str(etdFormat)
        bookLoanObj.save() 
        userUse.books_issued += 1
        quanBook.book_quantity -= 1
        userUse.save()
        quanBook.save()
        bookCheckoutNotification(user.email, bookLoanObj.book)    
        messages.info(request, "Book Successfully Issued")
        return redirect('profile', 'all')

    messages.info(request, "Book Cannot be Issued")
    return redirect('profile', 'all')

@login_required(login_url='login')
def renewBook(request, id):
    user = request.user
    if user.is_superuser:
        return redirect('adminLogin')

    loanBook = bookLoanDetail(user_id = user.id, book_id = id)
    if (loanBook.user_id == user.id and loanBook.book_id == id) and loanBook.return_status == 'pending':
        messages.info(request, 'Book Successfully Renewed')
        return redirect('profile', 'all')

    else:
        messages.info(request, "Book Cannot be Re-newed")
        return redirect('profile', 'all')

@login_required(login_url='login')
def reserveBook(request, id):
    user = request.user
    if user.is_superuser:
        return redirect('adminlLogin')

    bk = book.objects.get(pk = id)
    userLoanProfile = bookLoanDetail.objects.filter(user_id = user.id, book_id = id, return_status = 'pending')
    if bk.book_quantity == 0:
        if userLoanProfile:
            messages.info(request, 'You already Have this book')
            return redirect('profile', 'all')

        else:
            reserveBook = bookReservation(user_id = user.id, book_id = id)
            reserveBook.save()
            messages.info(request, 'Book Successfully Reserved, the user will recive a mail once the book is available')
            return redirect('profile', 'all')

    messages.info(request, 'Book Cannot Be Issued')
    return render('profile', 'all')