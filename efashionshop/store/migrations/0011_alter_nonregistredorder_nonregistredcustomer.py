# Generated by Django 4.2.1 on 2023-08-31 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_nonregistredorder_nonregistredcustomer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonregistredorder',
            name='nonRegistredCustomer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.nonregistredcustomer'),
        ),
    ]
