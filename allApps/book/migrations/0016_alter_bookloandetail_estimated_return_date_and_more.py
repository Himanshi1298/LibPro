# Generated by Django 4.1.1 on 2022-10-04 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_alter_bookloandetail_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookloandetail',
            name='estimated_return_date',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='bookloandetail',
            name='return_date',
            field=models.DateField(default=None, null=True),
        ),
    ]
