# Generated by Django 4.2.1 on 2023-07-20 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(blank=True, default=1, max_length=2, null=True),
        ),
    ]
