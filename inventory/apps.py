from django.apps import AppConfig
from django.db.models.signals import post_save


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        from inventory.signals import create_stock
        from inventory.models import ProductInventory
        post_save.connect(create_stock, sender=ProductInventory)
        from inventory.signals import save_stock
        post_save.connect(save_stock, sender=ProductInventory)
