# Generated by Django 4.1.1 on 2022-10-01 19:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0004_alter_bookloandetail_book_alter_bookloandetail_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookFinePayDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(default=datetime.date.today)),
                ('payment_ammount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookFinePayDetail', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='bookFine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fine', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookFine', to='book.bookloandetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookFine', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
