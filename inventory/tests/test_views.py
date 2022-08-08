"""Test Inventory views."""
from django.test import TestCase, Client
from django.urls import reverse
from inventory.models import (
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


class TestUrls(TestCase):
    """Test Inventory Views."""

    def setUp(self):
        """Set up the test."""
        self.category1 = Category.objects.create(
            name='Clothing',
            slug='clothing',
            is_active=False,
        )
        self.category2 = Category.objects.create(
            name='Food',
            slug='food',
            is_active=True,
        )
        self.tag1 = Tag.objects.create(
            name='skirt',
            slug='skirt',
            is_active=True,
        )
        self.tag2 = Tag.objects.create(
            name='shirt',
            slug='shirt',
            is_active=False,
        )
        self.brand1 = Brand.objects.create(
            name='Nike',
            slug='nike',
            is_active=True,
        )
        self.brand2 = Brand.objects.create(
            name='Adidas',
            slug='adidas',
            is_active=False,
        )
        self.product1 = Product.objects.create(
            name='Nike Skirt',
            slug='nike-skirt',
            description='Nike Skirt',
            category=self.category1,
            brand=self.brand1,
            is_active=True,
        )
        self.product1.tags.add(self.tag1)
        self.product2 = Product.objects.create(
            name='Adidas Shirt',
            slug='Adidas-Shirt',
            description='Adidas Shirt',
            category=self.category2,
            brand=self.brand2,
            is_active=False,
        )
        self.product2.tags.add(self.tag2)
        self.product_image1 = ProductImage.objects.create(
            product=self.product1,
            alt_text='Nike Skirt',
            is_active=True,
        )
        self.product_image2 = ProductImage.objects.create(
            product=self.product2,
            alt_text='Adidas Shirt',
            is_active=False,
        )
        self.product_attribute1 = ProductAttribute.objects.create(
            name='color',
            description='color'
        )
        self.product_attribute2 = ProductAttribute.objects.create(
            name='women clothing size',
            description='women clothing size'
        )
        self.product_type1 = ProductType.objects.create(
            name='women clothes',
            slug='women-clothes',
            description='women clothes'
        )
        self.product_type1.product_type_attributes.add(
            self.product_attribute1
        )
        self.product_type2 = ProductType.objects.create(
            name='men clothes',
            slug='men-clothes',
            description='men clothes'
        )
        self.product_type2.product_type_attributes.add(
            self.product_attribute2
        )
        self.product_attr_value1 = ProductAttributeValue.objects.create(
            product_attribute=self.product_attribute1,
            attribute_value='red'
        )
        self.product_attr_value2 = ProductAttributeValue.objects.create(
            product_attribute=self.product_attribute2,
            attribute_value='xs'
        )
        self.product_inventory1 = ProductInventory.objects.create(
            sku='11111',
            upc='11111',
            product=self.product1,
            product_type=self.product_type1,
            retail_price=10.00,
            store_price=11.00,
            sale_price=9.00,
            weight=float(1.0),
            is_active=True,
        )
        product_attr_value1 = ProductAttributeValue.objects.get(id=1)
        product_attr_value2 = ProductAttributeValue.objects.get(id=2)
        self.product_inventory1.attribute_values.set(
            [product_attr_value1, product_attr_value2],
        )
        self.product_inventory2 = ProductInventory.objects.create(
            sku='22222',
            upc='22222',
            product=self.product2,
            product_type=self.product_type1,
            retail_price=10.00,
            store_price=11.00,
            sale_price=9.00,
            weight=float(1.0),
            is_active=False,
        )
        self.product_inventory2.attribute_values.set(
            [product_attr_value1],
        )
        self.client = Client()
        self.products_list_url = reverse('products_list')
        self.product_detail_url = reverse(
            'product_detail',
            kwargs={'pk': 1}
        )

    def test_products_list_url(self):
        """Test product list url."""
        response = self.client.get(self.products_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['categories'].count(), 2)
        self.assertTemplateUsed(response, 'inventory/products_list.html')

    def test_product_list_search_query(self):
        """Test product list search query."""
        response = self.client.get(
            self.products_list_url,
            {'search_query': 'nike'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'][0], self.product1)
        self.assertTemplateUsed(response, 'inventory/products_list.html')

    def test_product_list_empty_query(self):
        """Test product list empty query."""
        response = self.client.get(
            self.products_list_url,
            {'search_query': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['products'][0],
            self.product2
        )
        self.assertTemplateUsed(response, 'inventory/products_list.html')

    def test_product_detail_url(self):
        """Test product detail url."""
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'].id, 1)
        self.assertTemplateUsed(response, 'inventory/product_detail.html')
        product_inventory_active = ProductInventory.objects.get(
            product=self.product1,
            is_active=True
        )
        attr = product_inventory_active.product_type.\
            product_type_attributes.all()
        self.assertEqual(attr.count(), 1)
        attribute_testing_set = set()
        for attribute in attr:
            attribute_testing_set.add(attribute.name)
        self.assertEqual(attribute_testing_set, {'color'})
        self.assertEqual(
            product_inventory_active.attribute_values.count(), 2
        )
        product_inventory_active_stock = Stock.objects.filter(
            product_inventory=product_inventory_active
        )
        self.assertEqual(product_inventory_active_stock.count(), 0)

    def test_check_if_product_has_stock(self):
        """Test if product has stock."""
        product_inventory_active = ProductInventory.objects.get(
            product=self.product1,
            is_active=True
        )
        product_inventory_active_stock = Stock.objects.filter(
            product_inventory=product_inventory_active
        )
        self.assertEqual(product_inventory_active_stock.count(), 0)
        # create stock
        stock = Stock.objects.create(
            product_inventory=product_inventory_active,
            units_variable=10,
            units=10,
            units_sold=0,
        )
        product_inventory_active_stock = Stock.objects.filter(
            product_inventory=product_inventory_active
        )
        self.assertEqual(product_inventory_active_stock.count(), 1)
        product_inventory_active_stock_list = list(
            product_inventory_active_stock
        )
        self.assertEqual(product_inventory_active_stock_list, [stock])
        attr = product_inventory_active.product_type.\
            product_type_attributes.all()
        self.assertEqual(attr.count(), 1)
        attribute_testing_set = set()
        for attribute in attr:
            attribute_testing_set.add(attribute.name)
        self.assertEqual(attribute_testing_set, {'color'})
        self.assertEqual(
            product_inventory_active.attribute_values.count(), 2
        )
        product_inventory_active_stock = Stock.objects.filter(
            product_inventory=product_inventory_active
        )
        self.assertEqual(product_inventory_active_stock.count(), 1)
        product_inventory_active_stock_list = list(
            product_inventory_active_stock
        )
        self.assertEqual(product_inventory_active_stock_list, [stock])
        self.assertEqual(
            product_inventory_active_stock_list[0].units_variable, 10
        )
        self.assertEqual(
            product_inventory_active_stock_list[0].units, 10
        )
        self.assertEqual(
            product_inventory_active_stock_list[0].units_sold, 0
        )
        self.assertEqual(
            product_inventory_active_stock_list[0].product_inventory,
            product_inventory_active
        )
        self.assertEqual(
            product_inventory_active_stock_list[0].product_inventory.
            product, self.product1
        )
        self.assertEqual(
            product_inventory_active_stock_list[0].product_inventory.
            product_type, self.product_type1
        )
        self.assertEqual(
            product_inventory_active_stock_list[0].product_inventory.
            product_type.product_type_attributes.count(), 1
        )
        unit = product_inventory_active_stock_list[0].product_inventory
        self.assertEqual(
            unit.product_type.product_type_attributes.all()[0],
            self.product_attribute1
        )
        attribute_testing_set.add(
            unit.product_type.product_type_attributes.all()[0]
        )
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['values_list'],
            [
                {
                    'color': 'red',
                    'Quantity': 10,
                    'Price': '9.00',
                    'id': 1
                }
            ]
        )
