# Generated by Django 3.2 on 2022-07-11 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_alter_stock_product_inventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(help_text='format: required, max_length=100', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.brand', verbose_name='Brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(help_text='format: required, max_length=100', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='productattributevalues',
            name='attributevalues',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributevalues', to='inventory.productattributevalue'),
        ),
        migrations.AlterField(
            model_name='productattributevalues',
            name='productinventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productattributevalues', to='inventory.productinventory'),
        ),
        migrations.AlterField(
            model_name='productinventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='inventory.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='producttypeattribute',
            name='product_attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productattribute', to='inventory.productattribute'),
        ),
        migrations.AlterField(
            model_name='producttypeattribute',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producttype', to='inventory.producttype'),
        ),
    ]
