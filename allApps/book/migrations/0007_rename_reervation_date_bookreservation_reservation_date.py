# Generated by Django 4.1.1 on 2022-10-02 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_bookreservation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookreservation',
            old_name='reervation_date',
            new_name='reservation_date',
        ),
    ]
