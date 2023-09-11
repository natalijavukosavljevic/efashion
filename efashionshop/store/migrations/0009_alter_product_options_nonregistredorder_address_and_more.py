# Generated by Django 4.2.1 on 2023-08-31 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_review_ownername'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-gender']},
        ),
        migrations.AddField(
            model_name='nonregistredorder',
            name='address',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='nonregistredorder',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='nonregistredorder',
            name='price',
            field=models.FloatField(blank=True, default=0),
        ),
    ]