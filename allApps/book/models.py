from datetime import date
from email.policy import default
from pyexpat import model
from . .userAccount.models import *
from django.utils.timezone import datetime


class bookCategory(models.Model):
    name      = models.CharField(max_length=150, null=True)
    createdOn = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.name)


class book(models.Model):
    book_title            = models.CharField(max_length=100, null=True)
    book_desc             = models.CharField(max_length=150, null=True)
    book_image            = models.ImageField(null=True, blank=True, upload_to="bookImage/")
    book_author           = models.CharField(max_length=100, null=True)
    book_category         = models.ForeignKey(bookCategory, related_name='books', on_delete=models.DO_NOTHING)
    about_book            = models.TextField(max_length=500, null=True)
    book_publication_date = models.DateTimeField(default=timezone.now)
    book_quantity         = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return str(self.book_title)

return_stat = (
    ("pending", "pending"),
    ("returned", "returned"),
)
class bookLoanDetail(models.Model):
    user                  = models.ForeignKey(User, related_name='bookLoanDetail', on_delete=models.CASCADE)
    book                  = models.ForeignKey(book, related_name='bookLoanDetail', on_delete=models.CASCADE)
    issue_date            = models.DateField(default=date.today)
    estimated_return_date = models.DateField(default=None)
    return_date           = models.DateField(default=None, null=True)
    return_status         = models.CharField(max_length = 10, choices = return_stat, default="pending")
    

    def __str__(self):
        return str(self.user)

class bookFine(models.Model):
    user         = models.ForeignKey(User, related_name='bookFine', on_delete=models.CASCADE)
    loan         = models.ForeignKey(bookLoanDetail, related_name="bookFine", on_delete=models.CASCADE)
    fine         = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return str(self.user)

class bookFinePayDetail(models.Model):
    user            = models.ForeignKey(User, related_name='bookFinePayDetail', on_delete=models.CASCADE)
    payment_date    = models.DateField(default=date.today)
    payment_ammount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.user)

class bookReservation(models.Model):
    user             = models.ForeignKey(User, related_name='bookReservation', on_delete=models.CASCADE)
    book             = models.ForeignKey(book, related_name='bookReservation', on_delete=models.CASCADE)
    reservation_date = models.DateField(default=date.today)

    def __str__(self):
        return str(self.user)