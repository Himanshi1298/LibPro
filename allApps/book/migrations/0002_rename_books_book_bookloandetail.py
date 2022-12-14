# Generated by Django 4.1.1 on 2022-10-01 17:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='books',
            new_name='book',
        ),
        migrations.CreateModel(
            name='bookLoanDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(default=datetime.date.today)),
                ('return_date', models.DateField(default=datetime.date.today)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookLoanDetail', to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookLoanDetail', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
