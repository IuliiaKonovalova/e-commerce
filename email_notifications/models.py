"""Models for email_notifications app."""
from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from inventory.models import Product, ProductAttributeValue
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
    code = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Code',
        help_text='Code.'
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
        return self.email_name

    def save(self, *args, **kwargs):
        super().save()
        users = Profile.objects.filter(subscription=True)
        recipients = [user.user.email for user in users]
        subject, from_email, to = (
            self.email_name, 'wowder', recipients
        )
        text_content = ''
        if self.code is not None:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p style="text-align:center; font-style: italic;">'
                'Only for our loyal customers!</p><br>'
                '<p>' + self.content + '</p><br>'
                '<p style="text-align:center"><em>Use the code below to get '
                'a special discount!</em></p>'
                '<br><br><p style="color:SlateBlue;'
                'background-color:Lavender; padding:1em 2em;'
                'text-align:center; font-weight:bold">' +
                self.code + '</p>'
                '<br><br><strong>Visit our shop now! </strong><br><br>'
                '<a href="https://wowder.onrender.com">'
                'Go to WoWder</a><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>WoWder shop</em>'
            )
        else:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p>' + self.content + '</p>'
                '<br><br><strong>Visit our shop now! </strong><br><br>'
                '<a href="https://wowder.onrender.com">'
                'Go to WoWder</a><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>WoWder shop</em>'
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


class StockEmailNotification(models.Model):
    """Model for stock email notifications."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Requested user',
        help_text='Requested user.'
    )
    requested_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Requested product',
        help_text='Requested product.',
        related_name='email_product'
    )
    requested_attributes_values = models.ManyToManyField(
        ProductAttributeValue,
        verbose_name='Requested attributes values',
        help_text='Requested attributes values.',
        related_name='email_attributes_values'
    )
    requested_quantity = models.PositiveIntegerField(
        verbose_name='Requested quantity',
        help_text='Requested quantity.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    answer_sent = models.BooleanField(
        default=False,
        verbose_name='Answer send',
        help_text='Answer send.'
    )

    class Meta:
        """Meta class for stock email notifications."""
        verbose_name = 'Stock email notification'
        verbose_name_plural = 'Stock email notifications'
        ordering = ['-created_at']

    def __str__(self):
        """Return the name of the stock email notification."""
        return self.user.username

    def get_all_not_sent(self):
        """Return all not send back to stock email notifications."""
        return StockEmailNotification.objects.filter(answer_sent=False)

    def get_all_requested_attributes_values_objects(self):
        """Return all requested attributes values objects."""
        all = self.requested_attributes_values.all()
        attr_values_string = ''
        for i in all:
            attr = str(i.product_attribute.name)
            value = str(i.attribute_value)
            attr_and_value = '\n ' + attr + ': ' + value
            attr_values_string += attr_and_value
        return attr_values_string

    def save(self, *args, **kwargs):
        super().save()
        subject, from_email, to = (
            'Stock email notification', 'wowder', [self.user.email]
        )
        text_content = ''
        html_content = (
            '<h1 style="color:indigo; text-align:center">'
            'Stock email notification</h1><br><strong>Your request has '
            'been sent to the administrator.</strong><br><p><strong>Product: '
            '</strong>' + self.requested_product.name + '</p><p><strong>'
            'Quantity: </strong>' + str(self.requested_quantity) + '</p>'
            '<br><br><strong>Visit our shop now! </strong><br><br>'
            '<a href="https://wowder.onrender.com">'
            'Go to WoWder</a><br><br>'
            '<p>Thank you for being with us!</p>'
            '<em>Wowder shop</em>'
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
