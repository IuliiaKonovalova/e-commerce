# Generated by Django 3.2 on 2022-06-08 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0006_alter_profile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(help_text='format: required, max_length=50', max_length=50, verbose_name='Country')),
                ('county_region', models.CharField(help_text='format: required, max_length=50', max_length=50, verbose_name='County/region')),
                ('city', models.CharField(help_text='format: required, max_length=50', max_length=50, verbose_name='City')),
                ('address_line', models.CharField(help_text='format: required, max_length=150', max_length=150, verbose_name='Address line')),
                ('postal_code', models.CharField(help_text='format: required, max_length=10', max_length=10, verbose_name='Postal code')),
                ('phone_number', models.CharField(help_text='format: required, max_length=15', max_length=15, verbose_name='Phone')),
                ('is_primary', models.BooleanField(default=False, help_text='format: not required', verbose_name='Is primary')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('user', models.ForeignKey(help_text='format: required', on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
