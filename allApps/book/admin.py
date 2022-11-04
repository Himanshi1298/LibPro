from django.contrib import admin
from . models import * 

admin.site.register(bookCategory)

@admin.register(book)
class book(admin.ModelAdmin):
    search_fields = ['book_title', 'book_author','book_publication_date']
    list_display = ("book_title", "book_category", "book_author", "book_publication_date", "book_quantity")


@admin.register(bookLoanDetail)
class bookLoanDetail(admin.ModelAdmin):
    search_fields = ['user', 'book']
    list_display = ("user", "book", "issue_date", "return_date", "estimated_return_date", "return_status")


admin.site.register(bookReservation)
admin.site.register(bookFine)
admin.site.register(bookFinePayDetail)