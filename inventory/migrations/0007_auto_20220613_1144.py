# Generated by Django 3.2 on 2022-06-13 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_producttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
            ],
            options={
                'verbose_name': 'Product attribute',
                'verbose_name_plural': 'Product attributes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_value', models.CharField(max_length=255)),
                ('product_attribute', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_attribute', to='inventory.productattribute')),
            ],
            options={
                'verbose_name': 'Product attribute value',
                'verbose_name_plural': 'Product attribute values',
                'ordering': ['attribute_value'],
            },
        ),
        migrations.CreateModel(
            name='ProductAttributeValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributevalues', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attributevaluess', to='inventory.productattributevalue')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(help_text='format: required, max_length=50', max_length=50, unique=True, verbose_name='Stock Keeping Unit')),
                ('upc', models.CharField(help_text='format: required, max_length=12', max_length=12, unique=True, verbose_name='Universal Product Code')),
                ('retail_price', models.DecimalField(decimal_places=2, help_text='format: required, the price must be between 0 and 9999999.99.', max_digits=9, verbose_name='Retail price')),
                ('store_price', models.DecimalField(decimal_places=2, help_text='format: required, the price must be between 0 and 9999999.99.', max_digits=9, verbose_name='Store price')),
                ('sale_price', models.DecimalField(decimal_places=2, help_text='format: required, the price must be between 0 and 9999999.99.', max_digits=9, verbose_name='Sale price')),
                ('weight', models.FloatField(verbose_name='Product weight')),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('attribute_values', models.ManyToManyField(related_name='product_attribute_values', through='inventory.ProductAttributeValues', to='inventory.ProductAttributeValue')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory', to='inventory.product', verbose_name='Product')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory', to='inventory.producttype', verbose_name='Product type')),
            ],
            options={
                'verbose_name': 'Product inventory',
                'verbose_name_plural': 'Product inventories',
                'ordering': ['product'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_checked', models.DateTimeField(blank=True, null=True)),
                ('units', models.IntegerField(default=0)),
                ('units_sold', models.IntegerField(default=0)),
                ('product_inventory', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='product_inventory', to='inventory.productinventory')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTypeAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_attribute', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='productattribute', to='inventory.productattribute')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='producttype', to='inventory.producttype')),
            ],
            options={
                'unique_together': {('product_attribute', 'product_type')},
            },
        ),
        migrations.AddField(
            model_name='productattributevalues',
            name='productinventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='productattributevaluess', to='inventory.productinventory'),
        ),
        migrations.AddField(
            model_name='producttype',
            name='product_type_attributes',
            field=models.ManyToManyField(related_name='product_type_attributes', through='inventory.ProductTypeAttribute', to='inventory.ProductAttribute'),
        ),
        migrations.AlterUniqueTogether(
            name='productattributevalues',
            unique_together={('attributevalues', 'productinventory')},
        ),
    ]
