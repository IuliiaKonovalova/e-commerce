# Generated by Django 3.2 on 2022-06-08 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, max_length=50, unique=True, blank=False', max_length=50, unique=True, verbose_name='Role name')),
                ('description', models.TextField(blank=True, help_text='format: not required, max_length=500', max_length=500, null=True, verbose_name='Role description')),
            ],
        ),
    ]
