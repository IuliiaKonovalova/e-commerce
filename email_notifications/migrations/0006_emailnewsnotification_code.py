# Generated by Django 3.2 on 2022-08-15 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_notifications', '0005_auto_20220630_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailnewsnotification',
            name='code',
            field=models.CharField(blank=True, help_text='Code.', max_length=100, null=True, verbose_name='Code'),
        ),
    ]