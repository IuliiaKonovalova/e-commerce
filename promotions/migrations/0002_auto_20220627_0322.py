# Generated by Django 3.2 on 2022-06-27 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='end_date',
            field=models.DateTimeField(verbose_name='End date'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start date'),
        ),
    ]
