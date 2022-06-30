"""Models for email_notifications app."""
from django.db import models
from django.core.mail import send_mail
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
        help_text='Requested product.'
    )
    requested_attributes_values = models.ManyToManyField(
        ProductAttributeValue,
        verbose_name='Requested attributes values',
        help_text='Requested attributes values.'
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
        
    def __str__(self):
        """Return the name of the stock email notification."""
        return self.user.username + ' ' + str(self.created_at)

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
            attr_and_value = '\n' + attr + ': ' + value
            attr_values_string += attr_and_value
        return attr_values_string

    def save(self, *args, **kwargs):
        super().save()
        users = Profile.objects.get(user=self.user)
        recipient_list = [self.user.email]
        product_attribute_values = ', '.join(product_attribute_values)
        content = 'Your request has been sent to the administrator.\n' \
                  'Product: ' + self.requested_product.name + '\n' \
                  'Quantity: ' + str(self.requested_quantity) + '\n' \

        if users.subscription:
            send_mail(
                'Stock email notification',
                content,
                'yuliyakonovalova5@gmail.com',
                recipient_list,
                fail_silently=False
            )
