# Generated by Django 4.1.1 on 2022-10-22 07:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0018_rename_book_isbn_book_bookisbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookloandetail',
            name='estimated_return_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
