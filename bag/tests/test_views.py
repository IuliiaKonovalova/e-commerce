"""Test Bag views."""
import datetime
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
)
from promotions.models import Promotion
from datetime import datetime
from django.utils import timezone


class TestBagViews(TestCase):
    """Test Bag views."""

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
        # create stock
        self.stock = Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=10,
            units=10,
            units_sold=0,
        )
        # Create promotion
        self.promotion = Promotion.objects.create(
            name='Promotion 1',
            slug='promotion-1',
            description='Promotion 1 description',
            promotion_code='PROMO1',
            promotion_reduction=10,
            start_date=datetime.now(),
            end_date=datetime.now() + timezone.timedelta(days=365 * 5),
            active=True,
        )
        self.promotion2 = Promotion.objects.create(
            name='Promotion 2',
            slug='promotion-2',
            description='Promotion 2 description',
            promotion_code='PROMO2',
            promotion_reduction=20,
            start_date=datetime.now(),
            end_date=datetime.now() + timezone.timedelta(days=365 * 5),
            active=True,
        )
        self.promotion2.products_inventory_in_promotion.add(
            self.product_inventory1
        )
        # urls
        self.client = Client()
        self.user = self.client.login(
            username='testuser',
            password='testpassword'
        )
        self.add_to_bag_url = reverse('add_to_bag')
        self.remove_item_url = reverse('remove_unit_from_bag')
        self.add_item_url = reverse('add_unit_to_bag')
        self.remove_all_item_units_url = reverse(
            'remove_all_item_units_from_bag'
        )
        self.remove_all_bag_items_url = reverse(
            'remove_all_bag'
        )
        self.apply_promo_code_url = reverse('apply_promo_code')

    def test_bag_display_view(self):
        """Test bag display view."""
        response = self.client.get(reverse('bag_display'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag_display.html')

    def test_bag_is_not_empty(self):
        """Test bag is not empty."""
        bag_items = []
        total = 0
        product_item_total = 0
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(self.client.session['bag'], {})
        # get data from the bag
        bag = self.client.session['bag']
        # check that it isinstance of dict: if isinstance(item_data, int):
        self.assertTrue(isinstance(bag, dict))
        # get product inventory by product_inventory_id from the dict
        product_inventory = ProductInventory.objects.get(id=bag['1'])
        # check that product_inventory is not None
        self.assertIsNotNone(product_inventory)
        #  check the quantity of the product
        self.assertEqual(bag['1'], 1)
        # check the product_item_total
        product_item_total = product_inventory.sale_price * bag['1']
        # count the total
        total = product_inventory.sale_price * bag['1']
        bag_items.append({
            'product_inventory': product_inventory,
            'product_item_total': product_item_total,
            'quantity': bag['1'],
        })

    def test_add_to_bag_ajax_view(self):
        """Test initialize bag clean session."""
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['bag'], {'1': 1})
        self.assertEqual(response.json()['success'], True)

    def test_add_to_bag_ajax_view_if_product_in_bag_already(self):
        """Test initialize bag clean session."""
        self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(self.client.session['bag'], {'1': 1})
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        # check if product_inventory_id 1 is in bag
        self.assertEqual(self.client.session['bag'], {'1': 2})
        self.assertEqual(response.json()['success'], True)

    def test_add_to_bag_if_quantity_is_more_than_stock_units(self):
        """Test initialize bag clean session."""
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 15},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['bag'], {'1': 10})
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['message_alert'],
            'Not enough units in stock. Only 10 added.'
        )

    def test_if_quantity_is_more_than_stock_units_item_was_in_bag(self):
        """Test initialize bag clean session."""
        self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 7},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(self.client.session['bag'], {'1': 7})
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 9},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(self.client.session['bag'], {'1': 10})
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['message_alert'],
            'Not enough units in stock. Only 3 added.'
        )

    def test_add_to_bag_ajax_view_failed(self):
        """Test initialize bag clean session."""
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_remove_item_ajax_view(self):
        """Test initialize bag clean session."""
        self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 2},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(self.client.session['bag'], {'1': 2})
        response = self.client.post(
            self.remove_item_url,
            {'product_inventory_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['bag'], {'1': 1})

    def test_remove_item_ajax_view_last_item(self):
        """Test initialize bag clean session."""
        self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(self.client.session['bag'], {'1': 1})
        response = self.client.post(
            self.remove_item_url,
            {'product_inventory_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['bag'], {})

    def test_remove_item_ajax_view_failed(self):
        """Test initialize bag clean session."""
        response = self.client.post(
            self.remove_item_url,
            {'product_inventory_id': 1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_add_item_to_bag_view(self):
        """Test initialize bag clean session."""
        response = self.client.post(
            self.add_item_url,
            {'product_inventory_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['message_alert'],
            'This product was not in the bag.'
        )
        self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(self.client.session['bag'], {'1': 1})
        response = self.client.post(
            self.add_item_url,
            {'product_inventory_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['bag'], {'1': 2})

    def test_add_item_to_bag_view_failed(self):
        """Test initialize bag clean session."""
        response = self.client.post(
            self.add_item_url,
            {'product_inventory_id': 1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_remove_all_item_units_from_bag_view(self):
        """Test initialize bag clean session."""
        self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(self.client.session['bag'], {'1': 1})
        response = self.client.post(
            self.remove_all_item_units_url,
            {'product_inventory_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['bag'], {})
        self.assertEqual(
            response.json()['message_alert'],
            'Nike Skirt REMOVED.'
        )

    def test_remove_all_item_units_from_empty_bag_view(self):
        response = self.client.post(
            self.remove_all_item_units_url,
            {'product_inventory_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['bag'], {})

    def test_remove_all_item_units_from_bag_view_failed(self):
        """Test initialize bag clean session."""
        response = self.client.post(
            self.remove_all_item_units_url,
            {'product_inventory_id': 1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_if_product_is_in_bag_with_quantity(self):
        """Test if product is in bag with quantity."""
        # test if product is in bag with quantity
        response = self.client.get(reverse('bag_display'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag_display.html')
        self.assertContains(response, '1')
        # add product to the bag
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 10},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        # check that bag session has 1 item
        self.assertEqual(len(self.client.session['bag']), 1)
        self.assertTrue(self.client.session['bag'], True)
        self.assertTrue(isinstance(self.client.session['bag'], dict))
        # loop through the bag and check the quantity and product_inventory_id
        for item in self.client.session['bag']:
            self.assertEqual(item, '1')
            self.assertEqual(self.client.session['bag'][item], 10)

    def test_remove_all_from_bag_view(self):
        """Test initialize bag clean session."""
        self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 7},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        response = self.client.post(
            self.remove_all_bag_items_url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['bag'], {})
        self.assertEqual(
            response.json()['message_alert'],
            'Bag is now empty.'
        )

    def test_remove_all_from_bag_view_failed(self):
        """Test initialize bag clean session."""
        response = self.client.post(
            self.remove_all_bag_items_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_apply_promo_code_ajax_view(self):
        """Test initialize bag clean session."""
        # Create promotion
        response = self.client.post(
            self.apply_promo_code_url,
            {'promo_code': 'PROMO1'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['total_promo'], '0')

    def test_apply_promo_code_ajax_view_failed(self):
        """Test initialize bag clean session."""
        # Create promotion
        response = self.client.post(
            self.apply_promo_code_url,
            {'promo_code': 'PROMO1'},
        )
        self.assertEqual(response.json()['success'], False)

    def test_update_bag_view_product_inventory_not_in_promotion(self):
        """Test initialize bag clean session."""
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['bag'], {'1': 1})
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['total_promo'], 0)
        response = self.client.post(
            self.apply_promo_code_url,
            {'promo_code': 'PROMO1'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['total_promo'], '9.00')

    def test_update_bag_view_product_inventory_in_promotion(self):
        """Test initialize bag clean session."""
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['bag'], {'1': 1})
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['total_promo'], 0)
        response = self.client.post(
            self.apply_promo_code_url,
            {'promo_code': 'PROMO2'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['total_promo'], '7.20')
        self.assertEqual(self.client.session['bag'], {'1': 1})

    def test_update_bag_view_product_inventory_not_in_active_promotion(self):
        """Test initialize bag clean session."""
        # set self.promotion to active=False
        self.promotion.active = False
        self.promotion.save()
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['bag'], {'1': 1})
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.client.session['total_promo'], 0)
        response = self.client.post(
            self.apply_promo_code_url,
            {'promo_code': 'PROMO1'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(self.client.session['total_promo'], 0)
