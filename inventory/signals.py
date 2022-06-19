"""Signals for the profiles app."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory.models import ProductInventory, Stock


@receiver(post_save, sender=ProductInventory)
def create_stock(sender, instance, created, **kwargs):
    if created:
        Stock.objects.create(product_inventory=instance)


@receiver(post_save, sender=ProductInventory)
def save_stock(sender, instance, **kwargs):
    instance.stock.save()