from dataclasses import Field
from datetime import date
from email.policy import default
from msilib.schema import File
from pyexpat import model
from . .userAccount.models import *
from django.utils.timezone import datetime
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File


class bookCategory(models.Model):
    name      = models.CharField(max_length=150, null=True)
    createdOn = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.name)


class book(models.Model):
    book_title             = models.CharField(max_length=100, null=True)
    book_desc              = models.CharField(max_length=150, null=True)
    bookIsbn               = models.CharField('ISBN', max_length=13, null=True)
    book_image             = models.ImageField(null=True, blank=True, upload_to="bookImage/")
    book_barcode           = models.ImageField(null=True, blank=True, upload_to="bookBarcode/")
    book_author            = models.CharField(max_length=100, null=True)
    book_category          = models.ForeignKey(bookCategory, related_name='books', on_delete=models.DO_NOTHING)
    about_book             = models.TextField(max_length=500, null=True)
    book_publication_date  = models.DateTimeField(default=timezone.now)
    book_quantity          = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return str(self.book_title)

    def save(self, *args, **kwargs):
        CODE_39 = barcode.get_barcode_class('code39')
        code = CODE_39(self.bookIsbn , writer=ImageWriter())
        buffer = BytesIO()
        code.write(buffer)
        self.book_barcode.save('isbn.png', File(buffer), save=False)
        return super().save(*args, **kwargs)


return_stat = (
    ("pending", "pending"),
    ("returned", "returned"),
)
class bookLoanDetail(models.Model):
    user                  = models.ForeignKey(User, related_name='bookLoanDetail', on_delete=models.CASCADE)
    book                  = models.ForeignKey(book, related_name='bookLoanDetail', on_delete=models.CASCADE)
    issue_date            = models.DateField(default=date.today)
    estimated_return_date = models.DateField(default=date.today)
    return_date           = models.DateField(null=True, blank=True)
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

reservation_stat = (
    ("reserved", "reserved"),
    ("alloted", "alloted"),
)
class bookReservation(models.Model):
    user             = models.ForeignKey(User, related_name='bookReservation', on_delete=models.CASCADE)
    book             = models.ForeignKey(book, related_name='bookReservation', on_delete=models.CASCADE)
    reservation_date = models.DateField(default=date.today)
    reservation_status    = models.CharField(max_length = 10, choices = reservation_stat, default="reserved")

    def __str__(self):
        return str(self.user)