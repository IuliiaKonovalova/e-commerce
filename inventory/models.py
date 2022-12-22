"""Models for the inventory app."""
from datetime import datetime, timedelta
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.db.models import F
from django.core.mail import EmailMultiAlternatives


class Category(models.Model):
    """Category model"""
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Category name',
        help_text='format: required, max_length=100'
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Category Slug',
        help_text='format: required, max_length=150'
    )
    is_active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )

    class Meta:
        """Meta class for Category model"""
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        """String representation of Category model"""
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @classmethod
    def get_active_categories(cls):
        """Get active categories"""
        return cls.objects.filter(is_active=True)

    @classmethod
    def get_not_active_categories(cls):
        """Get not active categories"""
        return cls.objects.filter(is_active=False)


class Tag(models.Model):
    """Tag model"""
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Tag name',
        help_text='format: required, max_length=100'
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Tag Slug',
        help_text='format: required, max_length=150'
    )
    is_active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )

    class Meta:
        """Meta class for Tag model"""
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        """String representation of Tag model"""
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @classmethod
    def get_active_tags(cls):
        """Get active tags"""
        return cls.objects.filter(is_active=True)

    @classmethod
    def get_not_active_tags(cls):
        """Get not active tags"""
        return cls.objects.filter(is_active=False)


class Brand(models.Model):
    """Brand model"""
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Brand name',
        help_text='format: required, max_length=100'
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Brand Slug',
        help_text='format: required, max_length=150'
    )
    description = models.TextField(
        max_length=500,
        null=False,
        blank=False,
        verbose_name='Brand description',
        help_text='format: required, max_length=500'
    )
    is_active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )

    class Meta:
        """Meta class for Brand model"""
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        ordering = ['name']

    def __str__(self):
        """String representation of the model"""
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @classmethod
    def get_active_brands(cls):
        """Get active brands"""
        return cls.objects.filter(is_active=True)

    @classmethod
    def get_not_active_brands(cls):
        """Get not active brands"""
        return cls.objects.filter(is_active=False)


class Product(models.Model):
    """Product model"""
    name = models.CharField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Product name',
        help_text='format: required, max_length=100'
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Product Slug',
        help_text='format: required, max_length=150'
    )
    description = models.TextField(
        max_length=500,
        null=False,
        blank=False,
        verbose_name='Product description',
        help_text='format: required, max_length=500'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Category',
        help_text='format: required, max_length=100'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='products',
        verbose_name='Tags',
        help_text='format: required, max_length=100'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Brand',
        help_text='format: required, max_length=100'
    )
    is_active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )

    class Meta:
        """Meta class for Product model"""
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        """String representation of Product model"""
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @classmethod
    def get_active_products(cls):
        """Get active products"""
        return cls.objects.filter(is_active=True).order_by('name')

    @classmethod
    def get_not_active_products(cls):
        """Get not active products"""
        return cls.objects.filter(is_active=False).order_by('name')

    def get_recently_created(self):
        """Get recently created products"""
        # if created 7 days ago, return True
        created_at = self.created_at.replace(tzinfo=None)
        return created_at >= datetime.now() - timedelta(days=7)

    def get_tags(self):
        """Get all tags of product"""
        return self.tags.all()

    def get_main_image(self):
        """Get main cover image of product"""
        images = ProductImage.objects.filter(product=self)
        if images.exists():
            active_images = images.filter(is_active=True)
            if active_images.exists():
                default_image = active_images.filter(default_image=True)
                if default_image.exists():
                    return default_image.first().image_url
                else:
                    return active_images.first().image_url
            return (
                'https://res.cloudinary.com/learning-coding/image/uploa' +
                'd/v1656240479/default_product_image.png'
            )
        else:
            return (
                'https://res.cloudinary.com/learning-coding/image/uploa' +
                'd/v1656240479/default_product_image.png'
            )

    def get_all_active_images(self):
        """Get all active images of product"""
        images = ProductImage.objects.filter(product=self)
        if images.exists():
            return images.filter(is_active=True).count()
        else:
            return False

    def get_out_of_stock(self):
        """Get out of stock products"""
        active_sales_prices = ProductInventory.objects.filter(
            product=self
        ).filter(is_active=True)
        if active_sales_prices.exists():
            return False
        else:
            return True

    def get_same_sale_price(self):
        """Get same sale price products"""
        active_sales_prices = ProductInventory.objects.filter(
            product=self
        ).filter(is_active=True)
        if active_sales_prices.exists():
            if active_sales_prices.count() == 1:
                return True
            else:
                sale_prices = []
                for sale_price in active_sales_prices:
                    sale_prices.append(float(sale_price.sale_price))
                if len(set(sale_prices)) == 1:
                    return True
                else:
                    return False
        else:
            return False

    def get_sale_price_is_lower_than_store_price(self):
        """Get sale price is lower than store price products"""
        active_sales_prices = ProductInventory.objects.filter(
            product=self
        ).filter(is_active=True)
        if active_sales_prices.exists():
            sale_store_prices_set = set()
            for sale_price in active_sales_prices:
                if float(sale_price.sale_price) < float(
                    sale_price.store_price
                ):
                    sale_store_prices_set.add(True)
            if True in sale_store_prices_set:
                return True
            else:
                return False
        else:
            return False

    def get_lowest_price(self):
        """Get lowest price of product"""
        active_sales_prices = ProductInventory.objects.filter(
            product=self
        ).filter(is_active=True)
        if active_sales_prices.exists():
            lowest_price = active_sales_prices.order_by('sale_price').first()
            return lowest_price.sale_price
        else:
            return None

    def get_highest_price(self):
        """Get highest price of product"""
        active_sales_prices = ProductInventory.objects.filter(
            product=self
        ).filter(is_active=True)
        if active_sales_prices.exists():
            highest_price = active_sales_prices.order_by('-sale_price').first()
            return highest_price.sale_price
        else:
            return None

    def get_lowest_store_price(self):
        """Get lowest price of product"""
        active_sales_prices = ProductInventory.objects.filter(
            product=self
        ).filter(is_active=True)
        if active_sales_prices.exists():
            lowest_price = active_sales_prices.order_by('store_price').first()
            return lowest_price.store_price
        else:
            return None

    def get_highest_store_price(self):
        """Get highest price of product"""
        active_sales_prices = ProductInventory.objects.filter(
            product=self
        ).filter(is_active=True)
        if active_sales_prices.exists():
            highest_price = active_sales_prices.order_by(
                '-store_price'
            ).first()
            return highest_price.store_price
        else:
            return None

    def get_all_inventory(self):
        """Get all inventory of product"""
        return ProductInventory.objects.filter(product=self)

    def get_average_rating(self):
        """Get average rating of product"""
        all_ratings = self.reviews.all()
        total = 0
        for rating in all_ratings:
            total += int(rating.rating)
        if len(all_ratings) > 0:
            return total / len(all_ratings)
        else:
            return 0


class ProductImage(models.Model):
    """Product image model"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Product',
        help_text='format: required, max_length=100'
    )
    image = CloudinaryField(
        'product_image',
        folder='product_images',
        null=True,
        blank=True,
    )
    alt_text = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        unique=False,
        verbose_name='Alt text',
        help_text='format: required, max_length=300'
    )
    default_image = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )

    class Meta:
        """Meta class for Product image model"""
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'
        ordering = ['product']

    def __str__(self):
        """String representation of Product image model"""
        return self.product.name

    def save(self, *args, **kwargs):
        """Check if there is a default image"""
        super().save(*args, **kwargs)
        if self.default_image:
            for image in self.product.images.all().exclude(id=self.id):
                image.default_image = False
                image.save()

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return 'static/images/default_product_image.png'

    @classmethod
    def get_active_product_images(cls):
        """Get active product images"""
        return cls.objects.filter(is_active=True)

    @classmethod
    def get_not_active_product_images(cls):
        """Get not active product images"""
        return cls.objects.filter(is_active=False)


class ProductAttribute(models.Model):
    """Product attribute model"""
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        max_length=500,
        blank=True,
    )

    class Meta:
        """Meta class for Product attribute model"""
        verbose_name = 'Product attribute'
        verbose_name_plural = 'Product attributes'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """Product type model"""
    name = models.CharField(
        max_length=100,
        null=True,
        unique=True,
        blank=True,
        verbose_name='Product type name',
        help_text='format: required, max_length=100'
    )
    slug = models.SlugField(
        max_length=150,
        null=True,
        unique=True,
        blank=True,
        verbose_name='Product type Slug',
        help_text='format: required, max_length=150'
    )
    product_type_attributes = models.ManyToManyField(
        ProductAttribute,
        related_name="product_type_attributes",
        through="ProductTypeAttribute",
    )
    description = models.TextField(
        max_length=500,
        null=False,
        blank=False,
        verbose_name='Product type description',
        help_text='format: required, max_length=500'
    )

    class Meta:
        """Meta class for Product type model"""
        verbose_name = 'Product type'
        verbose_name_plural = 'Product types'
        ordering = ['name']

    def __str__(self):
        """String representation of Product type model"""
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_product_type_attributes(self):
        """Get all product type attributes"""
        return self.product_type_attributes.all()


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_attribute",
        on_delete=models.PROTECT,
    )
    attribute_value = models.CharField(
        max_length=255,
    )

    class Meta:
        """Meta class for Product attribute value model"""
        verbose_name = 'Product attribute value'
        verbose_name_plural = 'Product attribute values'
        ordering = ['attribute_value']

    def __str__(self):
        """String representation of Product attribute value model"""
        return self.attribute_value


class ProductInventory(models.Model):
    """Product inventory model"""
    sku = models.CharField(
        max_length=50,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Stock Keeping Unit',
        help_text='format: required, max_length=50'
    )
    upc = models.CharField(
        max_length=12,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Universal Product Code',
        help_text='format: required, max_length=12'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory',
        verbose_name='Product',
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        related_name='inventory',
        verbose_name='Product type',
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="product_attribute_values",
        through="ProductAttributeValues",
    )
    retail_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
    )
    store_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
    )
    sale_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
    )
    weight = models.FloatField(
        null=False,
        blank=False,
        unique=False,
        verbose_name='Product weight',
    )
    is_active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )

    class Meta:
        """Meta class for Product inventory model"""
        verbose_name = 'Product inventory'
        verbose_name_plural = 'Product inventories'
        ordering = ['sku']

    def __str__(self):
        """String representation of Product inventory model"""
        return self.upc + ' - ' + self.sku

    def get_all_attribute_values_str(self):
        """Get all attribute values as string"""
        attribute_values_str = ''
        for attribute_value in self.attribute_values.all():
            attr = str(attribute_value.product_attribute.name)
            value = str(attribute_value.attribute_value)
            attribute_values_str += attr + ': ' + value + ' '
        return attribute_values_str

    @classmethod
    def get_active_product_inventories(cls):
        """Get active product inventories"""
        return cls.objects.filter(is_active=True)

    @classmethod
    def get_not_active_product_inventories(cls):
        """Get not active product inventories"""
        return cls.objects.filter(is_active=False)

    def get_attribute_values(self):
        """Get all attribute values for a product inventory"""
        return self.attribute_values.all()


class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name="stock",
        on_delete=models.SET_NULL,
        unique=False,
        null=True,
    )
    last_checked = models.DateTimeField(
        null=True,
        blank=True,
    )
    units_variable = models.IntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name='Units variable',
    )
    units = models.IntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name='Units current',
    )
    units_sold = models.IntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name='Units sold',
    )

    class Meta:
        """Meta class for Stock model"""
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ['product_inventory']

    def __str__(self):
        """String representation of Stock model"""
        # check if product inventory is null
        if self.product_inventory is None and self.units > 0:
            return 'No SKU: ' + str(self.id)
        elif self.units > 0:
            return (
                self.product_inventory.sku + ' - ' + str(self.units)
            )
        else:
            return (
                self.product_inventory.sku + ' - ' + 'Out of stock'
            )

    def save(self, *args, **kwargs):
        """reset product inventory is active in ProductInventory model"""
        super().save(*args, **kwargs)
        if self.units < 0 or self.units == 0:
            self.product_inventory.is_active = False
            self.product_inventory.save()
        # get self.product_inventory product
        product = self.product_inventory.product
        # get self.product_inventory attribute_values
        attribute_values = self.product_inventory.attribute_values.all()
        product_attribute_values_ids = [
            product_attribute_value.id for
            product_attribute_value in attribute_values
        ]
        product_attribute_values_ids.sort()
        # get all stock emails for this product
        all_emails = product.email_product.all()
        # set users' emails list
        users_to_send_email = []
        for email in all_emails:
            # check whether the answer wasn't sent yet
            if email.answer_sent is False:
                all_attr_values = email.requested_attributes_values.all()
                email_attribute_values_ids = [
                    product_attribute_value.id for
                    product_attribute_value in all_attr_values
                ]
                email_attribute_values_ids.sort()
                # check whether the attribute values are the same
                if email_attribute_values_ids == product_attribute_values_ids:
                    if email.requested_quantity <= self.units:
                        # get users
                        users_to_send_email.append(email.user.email)
                        email.answer_sent = True
                        email.save()
        recipients = list(users_to_send_email)
        # # if there are any requests, send email to users
        if len(recipients) > 0:
            subject, from_email, to = (
                'Stock notification', 'wowder', recipients
            )
            text_content = ''
            html_content = (
                '<h1 style="color:indigo; text-align:center">'
                'Stock email notification</h1><br><p>Product: '
                '<strong>' + self.product_inventory.product.name + '</strong>'
                ' is now in stock.</p><br><br><strong>Visit our shop '
                'to purchase! </strong><br><br><a '
                'href="https://wowder.onrender.com">'
                'Go to WoWder</a><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>WoWder shop</em>'
            )
            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    @classmethod
    def get_high_sales_fewer_products(cls):
        """get stocks where units < units_sold"""
        return cls.objects.filter(units__lt=F('units_sold'))

    @classmethod
    def get_units_inconsistent(cls):
        """compare unit variable with the some of unit+units_sold"""
        return cls.objects.filter(
            units_variable__gt=F('units') + F('units_sold')
        )

    @classmethod
    def get_low_stock_50(cls):
        """get stocks where units < 50"""
        return cls.objects.filter(units__lte=50)

    @classmethod
    def get_low_stock_20(cls):
        """get stocks where units < 20"""
        return cls.objects.filter(units__lte=20)

    @classmethod
    def get_low_stock_10(cls):
        """get stocks where units < 10"""
        return cls.objects.filter(units__lte=10)

    @classmethod
    def get_out_of_stock(cls):
        """get stocks where units = 0"""
        return cls.objects.filter(units=0)

    @classmethod
    def get_low_sales(cls):
        """get stocks where sales should be increased"""
        low_sale = cls.objects.filter(units_sold__gt=0)
        return low_sale.filter(units__gte=F('units_sold') * 5)


class ProductAttributeValues(models.Model):
    attributevalues = models.ForeignKey(
        ProductAttributeValue,
        related_name="attributevalues",
        on_delete=models.CASCADE,
    )
    productinventory = models.ForeignKey(
        ProductInventory,
        related_name="productattributevalues",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (("attributevalues", "productinventory"),)


class ProductTypeAttribute(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="productattribute",
        on_delete=models.CASCADE,
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name="producttype",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (("product_attribute", "product_type"),)
