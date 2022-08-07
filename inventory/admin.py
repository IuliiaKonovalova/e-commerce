"""Admin for the Inventory app."""
from django.contrib import admin
from .models import (
    Category,
    Tag,
    Brand,
    Product,
    ProductImage,
    ProductType,
    ProductAttribute,
    ProductAttributeValue,
    ProductInventory,
    Stock,
    ProductAttributeValues,
    ProductTypeAttribute,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for the Category model."""
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('name', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for the Tag model."""
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('name', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin for the Brand model."""
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('name', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for the Product model."""
    list_display = (
        'name',
        'slug',
        'category',
        'get_tags',
        'brand',
        'is_active',
    )
    list_filter = ('name', 'is_active', 'category', 'brand')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin for the ProductImage model."""
    list_display = ('product', 'image', 'is_active', 'default_image')
    list_filter = ('product', 'is_active', 'default_image')
    search_fields = ('product',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """Admin for the ProductAttribute model."""
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    """Admin for the ProductType model."""
    list_display = ('name', 'slug', 'get_product_type_attributes')
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    """Admin for the ProductAttributeValue model."""
    list_display = ('product_attribute', 'attribute_value')
    list_filter = ('product_attribute', 'attribute_value')
    search_fields = ('product_attribute', 'attribute_value')


@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    """Admin for the ProductInventory model."""
    list_display = (
        'sku',
        'upc',
        'product',
        'product_type',
        'retail_price',
        'store_price',
        'sale_price',
        'weight',
        'is_active',
        'get_all_attribute_values_str',
    )
    list_filter = ('product', 'product_type', 'is_active')
    search_fields = ('sku', 'upc', 'product', 'product_type')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """Admin for the Stock model."""
    list_display = (
        'product_inventory',
        'units_variable',
        'units',
        'units_sold'
    )
    list_filter = (
        'product_inventory',
    )
    search_fields = ('product_inventory',)


@admin.register(ProductAttributeValues)
class ProductAttributeValuesAdmin(admin.ModelAdmin):
    """Admin for the ProductAttributeValues model."""
    list_display = (
        'attributevalues',
        'productinventory',
    )
    list_filter = (
        'attributevalues',
        'productinventory',
    )
    search_fields = (
        'attributevalues',
        'productinventory',
    )


@admin.register(ProductTypeAttribute)
class ProductTypeAttributeAdmin(admin.ModelAdmin):
    """Admin for the ProductTypeAttribute model."""
    list_display = (
        'product_attribute',
        'product_type',
    )
    list_filter = (
        'product_attribute',
        'product_type',
    )
    search_fields = (
        'product_attribute',
        'product_type',
    )
