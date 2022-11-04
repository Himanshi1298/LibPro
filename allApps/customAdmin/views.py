from operator import truediv
from pickle import FALSE, NONE
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . .book.models import *
from . .book.forms import *
from . .userAccount.models import *
from . .userAccount.forms import *
from datetime import date, timedelta 
from django.db.models import Q
import schedule
import time
from django.core.mail import send_mail
from django.conf import settings 

# Create your views here.
def customAdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('adminHome')     
            else:
                messages.warning(request, 'You are not authorized for the Admin Login')
    
        else:
            messages.info(request, 'Username or Password Is Incorrect')

    return render(request, 'adminLogin.html')

@login_required(login_url='adminLogin')
def customAdminLogout(request):
    logout(request)
    return redirect('adminLogin')

@login_required(login_url='adminLogin')
def adminHome(request):
    user = request.user
    if user.is_superuser:
        messages.warning(request, "You are not authorized to access this page! Please Login at user portal")
        return render(request, 'adminHome.html')
    else:
        return redirect('login')

# pending work
@login_required(login_url='adminLogin')
def specificSearch(request, appModule):
    user = request.user
    if not user.is_superuser:
        messages.warning(request, "You are not authorized to access this page! Please Login at user portal")
        return redirect('login')
    
    if appModule == 'bookCategories':
        query   = request.GET['query']
        lookups = Q(name__icontains = query) | Q(createdOn__icontains = query)
        catBook = bookCategory.objects.filter(lookups)
        context = {
            'catBook'   : catBook,
            'appModule' : appModule, 
        }
        return render(request, 'searchUser.html', context)

    elif appModule == 'bookSearch':
        query = request.GET['query']
        lookups = Q(book_title__icontains = query) | Q(bookIsbn__icontains = query)
        bk = book.objects.filter(lookups)
        context = {
            'bk' : bk,
        }
        return render(request, 'issueForUser.html', context)

    elif appModule == 'userProfiles':
        query   = request.GET['query']
        lookups = Q(username__icontains = query) | Q(email__icontains = query)
        allUser = User.objects.filter(lookups).exclude(is_superuser = True)
        context = {
            'allUser'   : allUser,
            'appModule' : appModule, 
        }
        return render(request, 'searchUser.html', context)

    elif appModule == 'bookFinePayment':
        query = request.GET['query']
        # user
        lookups =  Q(payment_date__icontains = query) | Q(payment_ammount__icontains = query)
        bookFinePayment = bookFinePayDetail.objects.filter(lookups)
        context = {
            'bookFinePayment' : bookFinePayment,
            'appModule'       : appModule,
        }
        return render(request, 'searchUser.html', context)

    elif appModule == 'bookFines':
        query = request.GET['query']
        lookups = Q(fine__icontains = query) 
        bkFine = bookFine.objects.filter(lookups)
        context = {
            'bkFine' : bkFine,
            'appModule' : appModule,
        } 
        return render(request, 'searchUser.html', context)

    elif appModule == 'bookLoan':
        query = request.GET['query']
        lookups = Q(issue_date__icontains = query) | Q(estimated_return_date__icontains = query) | Q(return_date__icontains = query) | Q(return_status__icontains = query)
        loanDetail = bookLoanDetail.objects.filter(lookups)
        context = {
            'loanDetail' : loanDetail,
            'appModule' : appModule,
        } 
        return render(request, 'searchUser.html', context)

    elif appModule == 'book':
        query = request.GET['query']
        lookups = Q(book_title__icontains = query) | Q(book_author__icontains = query) | Q(bookIsbn__icontains = query) | Q(book_publication_date__icontains = query)
        allBook = book.objects.filter(lookups)
        context = {
            'allBook' : allBook,
            'appModule' : appModule,
        } 
        return render(request, 'searchUser.html', context)

    return redirect('adminHome')

    

@login_required(login_url='adminLogin')
def addModel(request, appModule): 
    user = request.user
    if not user.is_superuser:
        messages.warning(request, "You are not authorized to access this page! Please Login at user portal")
        return redirect('login')
   
    bookForm = curdBookForm()
    bookCatForm = curdBookCategories()
    if request.method == 'POST':
        bookCatForm = curdBookCategories(request.POST)
        bookForm = curdBookForm(request.POST, request.FILES)
        if 'bookCat' in request.POST:
            bookCatForm.save()
            return redirect('adminHome')
        
        if 'book' in request.POST:
            bookForm.save()    
            return redirect('adminHome')

    context = {
        'bookForm'    : bookForm,
        'bookCatForm' : bookCatForm,
        'appModule'   : appModule,
    }
    return render(request, 'addModel.html', context)

@login_required(login_url='adminLogin')
def changeModel(request, appModule, id):
    user = request.user
    if not user.is_superuser:
        messages.warning(request, "You are not authorized to access this page! Please Login at user portal")
        return redirect('login')
        
    try:
        bk = book.objects.get(pk = id)
    except:
        bk = NONE

    try:    
        bookCat = bookCategory.objects.get(pk = id)
    except:
        bookCat = NONE

    if bk is not NONE:
        bookForm = curdBookForm(instance=bk)
    else:
        bookForm = NONE
        
    if bookCat is not NONE:
        bookCatForm = curdBookCategories(instance=bookCat)
    else:
        bookCatForm = NONE

    if request.method == 'POST':
        if 'bookCat' in request.POST:
            bookCat.name = request.POST.get('name')
            bookCat.createdOn = request.POST.get('createdOn')
            bookCat.save()
            return redirect('adminHome')
        
        else:
            bk.book_title = request.POST.get('book_title')
            bk.book_desc  = request.POST.get('book_desc')
            bk.about_book = request.POST.get('about_book')
            image         = request.FILES.get('book_image')
        
            if image:
                bk.book_image = request.FILES.get('book_image')

            bk.book_author = request.POST.get('book_author')
            bk.bookIsbn    = request.POST.get('bookIsbn')
            bk.book_publication_date = request.POST.get('book_publication_date')
            bk.book_quantity = request.POST.get('book_quantity')
            bk.save()
            return redirect('adminHome')

    context = {
        'bookForm'    : bookForm,
        'bookCatForm' : bookCatForm,
        'appModule'   : appModule,
    }
    return render(request, 'addModel.html', context)


@login_required(login_url='adminLogin')
def listDisplay(request, appName, appModule):
    user = request.user
    if user.is_superuser:
        if appName == 'book':
            allBook = book.objects.all()
            loanDetail = bookLoanDetail.objects.all()
            bookCat = bookCategory.objects.all()
            bookFinePayment = bookFinePayDetail.objects.all()
            br = bookReservation.objects.all()
            bkFine = bookFine.objects.all()
            context = {
                    'allBook'             : allBook,
                    'loanDetail'          : loanDetail,
                    'bookCat'             : bookCat,
                    'bkFine'              : bkFine,
                    'bookFinePayment'     : bookFinePayment,
                    'appName'             : appName,
                    'appModule'           : appModule,
                    'br'                  : br,
            }
            return render(request, 'adminHome.html', context)

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
        messages.warning(request, "You are not authorized to access this page! Please Login at user portal")
        return redirect('login')


@login_required(login_url='adminLogin')
def userFormAll(request, id, st):
    user = request.user
    if not user.is_superuser:
        messages.warning(request, "You are not authorized to access this page! Please Login at user portal")
        return redirect('login')

    pgUser = User.objects.get(id = id)
    userProf = userProfiles.objects.get(user_id = id)
    userLinkProf = userlinks.objects.get(user_id = id)
    upForm = extendedProfileForm(instance=userProf)
    umForm = userProfileForm(instance=pgUser)
    ulForm = userLinksForm(instance=userLinkProf)
    foamUser = User.objects.get(pk = userProf.user_id)
    try:
        loanBook = bookLoanDetail.objects.all().filter(user_id = id)
    except bookLoanDetail.DoesNotExist:
        loanBook = NONE

    try:
        fineBook = bookFine.objects.all().filter(user_id = id)
    except:
        fineBook = NONE

    bk = book.objects.all()
    context = {
        'foamUser'     : foamUser, 
        'upForm'       : upForm,
        'ulForm'       : ulForm,
        'umForm'       : umForm,
        'loanBook'     : loanBook,
        'fineBook'     : fineBook,
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
            pgUser.first_name            = request.POST.get('first_name')
            image                        = request.FILES.get('user_profile_image')
            if image:
                userProf.user_profile_image  = request.FILES.get('user_profile_image')

            
            pgUser.save()
            return redirect('userFormAll', id, st)

        if formTwo == 'link-form':
            userLinkProf.website = request.POST.get('website')
            userLinkProf.github  = request.POST.get('github')
            userLinkProf.twitter = request.POST.get('twitter')
            userLinkProf.linkdin = request.POST.get('linkdin')
            userLinkProf.save()
            return redirect('userFormAll', id, st)
      
    return render(request, 'renderForm.html', context)

@login_required(login_url='adminLogin')
def issueBookFor(request, id):
    user = request.user
    if not user.is_superuser:
        messages.warning(request, "You are not authorized to access this page! Please Login at user portal")
        return redirect('login')

    try:
        loanBook = bookLoanDetail.objects.all().filter(user_id = id)
    except bookLoanDetail.DoesNotExist:
        loanBook = NONE

    foamUser = User.objects.get(pk = id)
    bk = book.objects.all()

    context = {
        'foamUser' : foamUser,
        'loanBook' : loanBook,
        'bk'       : bk,
    }    
    return render(request, 'issueForUser.html', context)


@login_required(login_url='adminLogin')
def returnBookFor(request, uid, bid):
    user = request.user
    if not user.is_superuser:
        messages.warning(request, "You are not authorized to access this page! Please Login at user portal")
        return redirect('login')

    try:
        loanBook = bookLoanDetail.objects.get(user_id = uid, book_id = bid, return_status = "pending")
    except bookLoanDetail.DoesNotExist:
        loanBook = NONE

    bk = book.objects.get(pk = bid)
    foamUser = userProfiles.objects.get(user_id = uid)

    if loanBook:
        bk.book_quantity += 1
        foamUser.books_issued -= 1
        loanBook.return_status = "returned"
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        loanBook.return_date = str(d1)
        loanBook.save()
        bk.save()
        foamUser.save()
        messages.info(request, "Book Successfully Returned")
        return redirect('userFormAll', uid, 'returned')

    messages.info('Book Cannot Be Returned')
    return redirect('userFormAll', uid, 'all')

@login_required(login_url='adminLogin')
def renewBookFor(request, uid, bid):
    user = request.user
    if not user.is_superuser:
        return redirect('login')

    try:
        loanBook = bookLoanDetail.objects.get(user_id = uid, book_id = bid, return_status = "pending")
    except bookLoanDetail.DoesNotExist:
        loanBook = NONE
    
    if loanBook:
        etd = datetime.now() + timedelta(days=10)
        etdFormat = etd.strftime("%Y-%m-%d")
        d1 = datetime.now().strftime("%Y-%m-%d")
        loanBook.issue_date = str(d1)
        loanBook.estimated_return_date = str(etdFormat)
        loanBook.save()
        messages.success(request, 'Book Successfully Renewed')
        return redirect('userFormAll', uid, 'all')

    messages.info(request, 'The Book Cannot Be Renewed')
    return redirect('userFormAll', uid, 'all')


def reserveCheck():
    reserveCheck = bookReservation.objects.all()
    for i in reserveCheck:
        if i.reservation_status == 'reserved' and i.book.book_quantity > 0:
            subject = 'Reset Password'
        message = f'The book { i.book} is now available click on http://192.168.29.23:8000/book/{ i.book.id }/{ i.book.book_title }'
        email_from = settings.EMAIL_HOST_USER
        reciver_list = [i.user.email]
        send_mail(subject, message , email_from ,reciver_list)
        print('mailsent')

schedule.every(1).minutes.do(reserveCheck)

@login_required(login_url='adminLogin')
def reserBookFor(request, uid, bid):
    user = request.user
    if not user.is_superuser:
        return redirect('login')
    
    bk = book.objects.get(pk = bid)
    userLoanProfile = bookLoanDetail.objects.filter(user_id = uid, book_id = bid, return_status = 'pending')
    if bk.book_quantity == 0:
        if userLoanProfile:
            messages.info(request, 'You already Have this book')
            return redirect('userFormAll', uid, 'all')

        else:
            reserveBook = bookReservation(user_id = uid, book_id = bid)
            reserveBook.save()
            messages.info(request, 'Book Successfully Reserved, the user will recive a mail once the book is available')
            return redirect('userFormAll', uid, 'all')

@login_required(login_url='adminLogin')
def deleteSpecific(request, appModule, id):
    user = request.user
    if not user.is_superuser:
        return redirect('login')

    if appModule == 'userProfiles':
        foamUser = User.objects.get(pk = id)
        foamUser.is_active = False
        foamUser.save()
        messages.info(request, f'User {User.username}  successfully deleted')
        return redirect('/adminHome/book/userProfiles/listDisplay')

    elif appModule == 'book':
        bk = book.objects.get(pk = id)
        bk.delete()
        messages.info(request, f'Book {book.book_title} successfully deleted')
        return redirect('/adminHome/book/book/listDisplay')

    elif appModule == 'bookCategories':
        catBook = bookCategory.objects.get(pk = id)
        catBook.delete()
        messages.info(request, f'Category successfully deleted')
        return redirect('/adminHome/book/bookCategories/listDisplay')
        
    elif appModule == 'bookReservation':
        bookLoan = bookReservation.objects.get(pk = id)
        bookLoan.delete()
        messages.info(request, f'Book Loan successfully deleted')
        return redirect('/adminHome/book/bookReservation/listDisplay')

    return redirect('index.html')

@login_required(login_url='adminLogin')
def checkAndAction(request, uid, bid):
    user = request.user
    if not user.is_superuser:
        return redirect('login')
    try:
        loanBook = bookLoanDetail.objects.all().filter(user_id = uid, book_id = bid, return_status = 'pending')
    except bookLoanDetail.DoesNotExist:
        loanBook = NONE

    etd = datetime.now() + timedelta(days=10)
    etdFormat = etd.strftime("%Y-%m-%d")
    loanInsert = bookLoanDetail(user_id = uid, book_id = bid, estimated_return_date = etdFormat)
    bk         = book.objects.get(pk = bid)
    foamUser   = userProfiles.objects.get(user_id = uid)

    if loanBook:
        messages.warning(request, 'You already have this book')
        return redirect('issueBookFor', uid)

    
    elif foamUser.books_issued >= 5:
        messages.warning(request, 'Maximum 5 books can be issued at a time, please return some to issue new books')
        return redirect('issueBookFor', uid)
        

    foamUser.books_issued += 1
    bk.book_quantity -= 1
    foamUser.save()
    bk.save()
    loanInsert.save()
    messages.info(request, 'Book Successfully Issued')
    return redirect('issueBookFor', uid)

    
