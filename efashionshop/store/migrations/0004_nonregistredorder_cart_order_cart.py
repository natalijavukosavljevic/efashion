# Generated by Django 4.2.1 on 2023-07-24 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_price_alter_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonregistredorder',
            name='cart',
            field=models.ManyToManyField(blank=True, to='store.productset'),
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ManyToManyField(blank=True, to='store.productset'),
        ),
    ]
