"""Tests for the models in the wishlist app."""
from django.test import TestCase
from inventory.models import (
    Category,
    Tag,
    Brand,
    Product,
)
from profiles.models import Role, User
from wishlist.models import Wishlist


class WishlistTestCase(TestCase):
    """Test case for the Wishlist model."""
    def setUp(self):
        """Set up the test case."""
        self.role1 = Role.objects.create(
            name='Customer',
            description='Customer'
        )
        self.role2 = Role.objects.create(
            name='Manager',
            description='Manager'
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

    def test_wishlist_creation(self):
        """Test wishlist creation."""
        # wishlist should already exist because of signals
        self.assertEqual(Wishlist.objects.count(), 2)
        self.assertEqual(Wishlist.objects.get(
            user=self.user
        ).user, self.user)
        self.assertEqual(
            Wishlist.objects.get(user=self.user2).user,
            self.user2
        )

    def test_wishlist_add_product(self):
        """Test wishlist add product."""
        # add products to wishlist
        self.assertTrue(
            Wishlist.objects.get(user=self.user).add_to_wishlist(
                self.product1
            )
        )
        self.assertTrue(
            Wishlist.objects.get(user=self.user).add_to_wishlist(
                self.product2
            )
        )
        # check that product is in the wishlist
        self.assertEqual(
            Wishlist.objects.get(user=self.user).products.count(), 2
        )

    def test_wishlist_str(self):
        """Test wishlist str."""
        self.assertEqual(
            str(Wishlist.objects.get(user=self.user)),
            'testuser\'s wishlist'
        )

    def test_wishlist_add_product_product_is_already_in_wishlist(self):
        """Test wishlist add product product is already in wishlist."""
        # add product to wishlist
        self.assertTrue(
            Wishlist.objects.get(user=self.user).add_to_wishlist(
                self.product1
            )
        )
        self.assertFalse(
            Wishlist.objects.get(user=self.user).add_to_wishlist(
                self.product1
            )
        )
        # check that product is in the wishlist
        self.assertEqual(
            Wishlist.objects.get(user=self.user).products.count(), 1
        )

    def test_wishlist_remove_product(self):
        """Test wishlist remove product."""
        # add product to wishlist
        self.assertTrue(
            Wishlist.objects.get(user=self.user).add_to_wishlist(
                self.product1
            )
        )
        self.assertTrue(
            Wishlist.objects.get(user=self.user).add_to_wishlist(
                self.product2
            )
        )
        # remove product from wishlist
        self.assertTrue(
            Wishlist.objects.get(user=self.user).remove_from_wishlist(
                self.product1
            )
        )
        self.assertEqual(
            Wishlist.objects.get(user=self.user).products.count(), 1
        )

    def test_wishlist_remove_product_product_is_not_in_wishlist(self):
        """Test wishlist remove product product is not in wishlist."""
        self.assertEqual(
            Wishlist.objects.get(user=self.user).products.count(), 0
        )
        # remove product from wishlist
        self.assertFalse(
            Wishlist.objects.get(user=self.user).remove_from_wishlist(
                self.product1
            )
        )
        # check that product is not in the wishlist
        self.assertEqual(
            Wishlist.objects.get(user=self.user).products.count(), 0
        )

    def test_wishlist_remove_all_from_wishlist(self):
        """Test wishlist remove all products."""
        # add products to wishlist
        self.assertTrue(
            Wishlist.objects.get(user=self.user).add_to_wishlist(
                self.product1
            )
        )
        self.assertTrue(
            Wishlist.objects.get(user=self.user).add_to_wishlist(
                self.product2
            )
        )
        # remove all products from wishlist
        self.assertTrue(
            Wishlist.objects.get(user=self.user).remove_all_from_wishlist()
        )
        # check that products are not in the wishlist
        self.assertEqual(
            Wishlist.objects.get(user=self.user).products.count(), 0
        )

    def test_wishlist_get_products(self):
        """Test wishlist get products."""
        # add products to wishlist
        self.assertTrue(
            Wishlist.objects.get(user=self.user).add_to_wishlist(
                self.product1
            )
        )
        self.assertTrue(
            Wishlist.objects.get(user=self.user).add_to_wishlist(
                self.product2
            )
        )
        self.assertQuerysetEqual(
            Wishlist.objects.get(user=self.user).get_products().all(),
            [self.product2, self.product1]
        )
