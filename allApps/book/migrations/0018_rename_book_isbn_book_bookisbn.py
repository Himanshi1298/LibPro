# Generated by Django 4.1.1 on 2022-10-21 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0017_book_book_barcode_book_book_isbn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='book_isbn',
            new_name='bookIsbn',
        ),
    ]
