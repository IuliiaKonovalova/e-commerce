"""Tests for email_notifications app."""
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from profiles.models import Role, Profile
from email_notifications.models import (
    EmailNewsNotification,
    StockEmailNotification
)
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


class EmailNewsNotificationTest(TestCase):
    """Tests for email news notifications."""
    def setUp(self):
        """Set up the test case."""
        # create users
        self.role1 = Role.objects.create(
            name='Customer',
            description='Customer'
        )
        self.role2 = Role.objects.create(
            name='Manager',
            description='Manager'
        )
        self.role3 = Role.objects.create(
            name='Admin',
            description='Admin'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='Password987',
            email='testuser@gmail.com'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='Password987',
            email='testuser2@gmail.com'
        )
        self.user3 = User.objects.create_user(
            username='testuser3',
            password='Password987',
            email='admin@gmail.com'
        )
        self.profile1 = Profile.objects.get(id=self.user.profile.id)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        # create product_inventories + stock
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

    def test_email_news_notification_str(self):
        """Test the email news notification string representation."""
        email_news_notification = EmailNewsNotification.objects.create(
            email_name='test_email_news_notification',
            content='test_content'
        )
        self.assertEqual(
            str(email_news_notification),
            'test_email_news_notification'
        )

    def test_email_news_notification_save(self):
        """Test the email news notification save method."""
        email_news_notification = EmailNewsNotification.objects.create(
            email_name='test_email_news_notification',
            content='test_content'
        )
        self.assertEqual(
            email_news_notification.email_name,
            'test_email_news_notification'
        )
        self.assertEqual(
            email_news_notification.content,
            'test_content'
        )

    def test_stock_email_notification_str(self):
        """Test the stock email notification string representation."""
        stock_email_notification = StockEmailNotification.objects.create(
            user=self.user,
            requested_product=self.product1,
            requested_quantity=1,
            answer_sent=False
        )
        stock_email_notification.save()
        self.assertEqual(
            str(stock_email_notification),
            'testuser'
        )

    def test_stock_email_notification_get_all_not_sent(self):
        """Test the stock email notification get all not sent method."""
        stock_email_notification = StockEmailNotification.objects.create(
            user=self.user,
            requested_product=self.product1,
            requested_quantity=1,
            answer_sent=False
        )
        stock_email_notification.save()
        self.assertEqual(
            stock_email_notification.get_all_not_sent()[0],
            stock_email_notification
        )

    def test_stock_email_notification_save(self):
        """Test the stock email notification save method."""
        stock_email_notification = StockEmailNotification.objects.create(
            user=self.user,
            requested_product=self.product1,
            requested_quantity=1,
            answer_sent=False
        )
        mail.send_mail(
            subject='subject',
            message='message',
            from_email='from@example.com',
            recipient_list=[(self.user.email)]
        )
        assert len(mail.outbox) == 2
        assert mail.outbox[1].subject == 'subject'
        assert mail.outbox[1].body == 'message'
        assert mail.outbox[1].from_email == 'from@example.com'
        assert mail.outbox[1].to == ['testuser@gmail.com']
        self.profile1.subscription = False
        self.profile1.save()

    def test_stock_email_notification_get_all_attributes_values(self):
        """Test get all attributes values from request"""
        stock_email_notification = StockEmailNotification.objects.create(
            user=self.user,
            requested_product=self.product1,
            requested_quantity=1,
            answer_sent=False
        )
        stock_email_notification.save()
        self.assertEqual(
            stock_email_notification.
            get_all_requested_attributes_values_objects(), ''
        )
        stock_email_notification.requested_attributes_values.add(
          self.product_attr_value1
        )
        self.assertEqual(
            stock_email_notification.
            get_all_requested_attributes_values_objects(),
            '\n color: red'
        )
