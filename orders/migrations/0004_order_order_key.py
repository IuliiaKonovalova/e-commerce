# Generated by Django 3.2 on 2022-07-11 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_order_key_order_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_key',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]