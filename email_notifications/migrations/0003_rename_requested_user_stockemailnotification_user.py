# Generated by Django 3.2 on 2022-06-29 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_notifications', '0002_stockemailnotification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockemailnotification',
            old_name='requested_user',
            new_name='user',
        ),
    ]