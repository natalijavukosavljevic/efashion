# Generated by Django 4.2.1 on 2023-08-31 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_options_nonregistredorder_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonregistredorder',
            name='nonRegistredCustomer',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='store.nonregistredcustomer'),
        ),
    ]
