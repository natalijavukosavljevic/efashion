# Generated by Django 4.2.1 on 2023-08-31 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_nonregistredorder_nonregistredcustomer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nonregistredorder',
            old_name='nonRegistredCustomer',
            new_name='nonRegCustomer',
        ),
    ]