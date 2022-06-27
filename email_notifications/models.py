"""Models for email_notifications app."""
from django.db import models
from django.core.mail import send_mail
from profiles.models import Profile



class EmailNewsNotification(models.Model):
    """Model for email news notifications."""
    email_name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email name',
        help_text='Email name.'
    )
    content = models.TextField(
        max_length=1500,
        null=False,
        blank=False,
        verbose_name='Content',
        help_text='Content.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    
    class Meta:
        """Meta class for email news notifications."""
        verbose_name = 'Email news notification'
        verbose_name_plural = 'Email news notifications'

    def __str__(self):
        """Return the name of the email news notification."""
        return self.email_name + ' ' + str(self.created_at)

    def save(self):
        super().save()
        users = Profile.objects.filter(subscription=True)
        recipients = [user.user.email for user in users]
        send_mail(
            self.email_name,
            self.content,
            'yuliyakonovalova5@gmail.com',
            recipients,
            fail_silently=False
        )
