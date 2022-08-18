# TESTING

## Automated testing

### Django unit testing

At the very beginning of the project, I decided to use Django's built-in unit testing framework. Thus, all tests are created simultaneously with the code.

I am running the following testing commands in my terminal to test the code:

```
python manage.py test <name of the app>
```

To create the coverage report, I run the following command:

```
coverage run --source=<name of the app> manage.py test
```

```
coverage report
```

To see the html version of the report and find out whether some pieces of code are missing, I run the following command:

```
coverage html
```

```
python3 -m http.server
```
**Bag app:**

![Django unit testing. Bag. Coverage](documentation/testing/coverage/coverage_bag.png)


However, after implementing the promotion functionality, I was not been able to get access to the full contexts.py and therefore I am missing 4 cases on the coverage report.

![Django unit testing. Promotions. Coverage](documentation/testing/coverage/coverage_promotions_2.png)


 The description of the testing iss is in is in the section [Django unit testing Issues](#django-unit-testing-issues) **Unsolved issues:**

**Email_notification app:**

![Django unit testing. Email_notification. Coverage](documentation/testing/coverage/coverage_email_notifications.png)


The missing coverage is due to the fact that I was not able to test fully ```EmailStockNotificationFormAJAX```. The description of the testing iss is in is in the section [Django unit testing Issues](#django-unit-testing-issues) **Unsolved issues:**

**Home app:**




**Inventory app:**

![Django unit testing. Inventory. Coverage](documentation/testing/coverage/coverage_inventory.png)



**Orders app:**

![Django unit testing. Orders. Coverage](documentation/testing/coverage/coverage_orders.png)

![Django unit testing. Orders. Coverage](documentation/testing/coverage/coverage_orders_missing_case.png)

Missing case due to the use of the function to update payment status. The description of the testing iss is in is in the section [Django unit testing Issues](#django-unit-testing-issues) **Unsolved issues:**

**Payment app:**

![Django unit testing. Payment. Coverage](documentation/testing/coverage/coverage_payment.png)


The missing cases in the coverage is simply because I have no idea how test webhooks. The functionality is working well and described in the section [Django unit testing Issues](#django-unit-testing-issues) **Unsolved issues:** 

![Django unit testing. Payment. Coverage. Missing cases](documentation/testing/coverage/coverage_payment_missing_cases.png)

**Personnel app:**





**Profiles app:**

![Django unit testing. Profiles. Coverage](documentation/testing/coverage/coverage_profiles.png)


The missing coverage is due to the fact that I was not able to test the edit profile view on the password form. The description of the view is in the section [Django unit testing Issues](#django-unit-testing-issues) **Unsolved issues:**


**Promotions app:**

![Django unit testing. Promotions. Coverage](documentation/testing/coverage/coverage_promotions.png)



**Reviews app:**

![Django unit testing. Reviews. Coverage](documentation/testing/coverage/coverage_reviews.png)


**Wishlist app:**

![Django unit testing. Wishlist. Coverage](documentation/testing/coverage/coverage_wishlist.png)

**Total coverage:**

![Django unit testing. Total coverage](documentation/testing/coverage/coverage_total.png)

### Django unit testing Issues

**Solved issues:**

1. I couldn't figure out how to test save methods in Address model as I was receiving the correct result in my print statements in the terminal but at the same time I was getting an error message.

![Calling save() for Address Model](documentation/testing/tests_issues1.png)

*Solution:*

rather than calling ```self.assertEqual(self.address2.is_primary, True)```, I created a separate variable for the ```address2``` and called it:

```python
  address2 = Address.objects.get(id=2)
  self.assertEqual(address2.is_primary, False)
```

![Calling save() for Address Model. Solution](documentation/testing/tests_issues2.png)

2. I couldn't add particular attributes for testing and couldn't receive the data in my print statement

![Testing many-to-many type](documentation/testing/tests_issues4.png)

*Solution:*

Considering the fact that Direct assignment of many-to-many types is not allowed, I retrieved the variables from `ProductAttributeValue` table and added them by assigned set() and putting all variables in square brackets. Additionally, when I was calling `attribute_values` field's values, I used `.all()


```python
    def setUp(self):
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

    def test_product_inventory_attribute_values_field(self):
        """Test the attribute values field"""
        print(self.product_inventory1.sku)
        print(self.product_inventory1.upc)
        print(self.product_inventory1.product)
        print(self.product_inventory1.product_type)
        print(self.product_inventory1.attribute_values.all())
```

3. I couldn't test unique constrain in ProductAttributeValues model as I was getting the error:

![Testing unique constrain](documentation/testing/tests_issues5.png)

*Solution:*

create a new object  ```product_attr_value3``` and a new variable: attributevlues by calling the ```ProductAttributeValue.objects.get()``` method with id of product_attr_value3. It is needed to prevent duplicate values from set_up method.
Then, I retrieved the ```productinventory``` by calling the ```ProductInventory.objects.get()``` method with id of self.product_inventory2 (self.product_inventory2 was created in the set_up method). After all, I created a new object for ProductAttrivuteVlaues model and assigned received values to it.

```python
    product_attr_value3 = ProductAttributeValue.objects.create(
        product_attribute=self.product_attribute1,
        attribute_value='yellow',
    )
    attributevalues=ProductAttributeValue.objects.get(
        id=product_attr_value3.id
    )
    productinventory=ProductInventory.objects.get(
        id=self.product_inventory2.id
    )
    original = ProductAttributeValues.objects.create(
        attributevalues=attributevalues,
        productinventory=productinventory
    )
```
To check whether the unique constrain is working, I called the following methods:

```python
    self.assertNotEquals(original, None)
    with self.assertRaises(Exception):
        original_clone = ProductAttributeValues.objects.create(
            attributevalues=attributevalues,
            productinventory=productinventory
        )
```
4. While testing ```ProductInventoryForm```, I was getting the following error:

![Testing ProductInventoryForm](documentation/testing/tests_issues6.png)

*Solution:*

As I figured out the error was coming from the form's fields: ```retail_price```, ```store_price```, ```sale_price```, which were added to widget's attributes.
DecimalField should be added to the widget's attributes. Thus, I deleted them and added them separately:

```python
    retail_price = forms.DecimalField()
    store_price = forms.DecimalField()
    sale_price = forms.DecimalField()
```
Additionally, while writing test cases to check whether ```ProductInventoryForm``` is valid, I was using float() for retail_price, store_price, sale_price, weight.

5. I couldn't test contexts.py file. I wasn't able to test the context of the bag view. I was trying to test the context of the bag view, but unsuccessful.

```python
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
    print('test contexts.py')
    print(self.client.session['bag'])
    self.assertTrue(isinstance(self.client.session['bag'], dict))
    # loop through the bag and check the quantity and product_inventory_id
    for item in self.client.session['bag']:
        print(item)
        print(self.client.session['bag'][item])
        self.assertEqual(item, '1')
        self.assertEqual(self.client.session['bag'][item], 10)
```

![Django unit testing. Bag. Missing Coverage](documentation/testing/coverage/coverage_bag_views_missing.png)

*Solution:*

I imported ```bag_contents``` into views.py file. and used to get the total spending and total quantity of the bag. This allowed me to include contexts.py file into the testing.

  
  ```python
    contents = bag_contents(request)
    total = contents['total']
    product_count = contents['product_count']
```




**Unsolved issues:**

1. I was getting an error message when I tried multiple times to test JsonResponse response on Password change.

![Django unit testing. Profiles. Coverage. Missing](documentation/testing/coverage/coverage_profiles_views_missing.png)

I have made the following steps to solve this issue:

```python
    from django.contrib.auth.hashers import make_password

            pwd = make_password('123')
        self.user33 = User.objects.create(
            username='testuser33',
            password = pwd,
            email='user3gmail.com'
        )
        self.client.force_login(self.user33)
        pwd2 = make_password('12345')
        print('User password', self.user33.password)
        print(pwd)
        print(pwd2)
        response = self.client.post(
            self.edit_user_profile_url,
            data={
                'form_type': 'password',
                'old_password': pwd,
                'new_password': pwd2,
                'confirm_password': pwd2
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
```
The following screenshot will confirm that the passwords in both cases were hashed and changed correctly.

![Testing JsonResponse on Password change](documentation/testing/tests_issues3.png)
As it might seem, I am not able to test the response of the JsonResponse.

2. I was getting an error message when I tested ```EmailStockNotificationFormAJAX```. This errors because testing wasn't working correctly as it wasn't confirming the existence of the ```self.product_inventory1``` and relevant ```self.attribute_values1``` and ```self.attribute_values2```.

![Django unit testing. Email notifications. Coverage. Missing](documentation/testing/coverage/coverage_email_notification_missing.png)

However, the view is working correctly. It is **checking** for the existence of the ```self.product_inventory1```. It loop through all possible product_inventories of a product and checking whether a product_inventory with received ```attribute_values``` are present in the table. If so, it returns this product_inventory and checks the units available. If there is enough units in stock, it doesn't send the email and returns an alert message to the page.

![Proof of correct functionality of EmailStockNotificationFormAJAX. Not enough in stock](documentation/testing/email_stock_view1.png)

![Proof of correct functionality of EmailStockNotificationFormAJAX. Enough in stock](documentation/testing/email_stock_view2.png)

3. I was getting an error when I was testing string method for stock model:

```python
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
```

![Django unit testing. Stock. Testing issue. String](documentation/testing/tests_issues9.png)

However, when I was testing string method in my template, I was getting the correct string for the stock with deleted product inventory.

```html
      {% for stock in all_stock %}
        {{ stock }}
      {% endfor %}
```

![Django unit testing. Stock. Testing issue. String](documentation/testing/tests_issues10.png)

4. This issue is regarding the importing context.py file. There are no errors in functionality but 3 missing cases are present

![Django unit testing. Profiles. Coverage. Missing-unsolved](documentation/testing/coverage/coverage_report_contexts.png)

5. I was not able to test webhooks in the payment ap. However, the functionality is working well. To proof that, I attached the following screenshots:

  - I have added products in the bag:

    ![Django unit testing. Payment. Coverage. Missing](documentation/testing/payment_1.png)

  - Click on checkout, then I was redirected to the payment page:

    ![Django unit testing. Payment. Coverage. Missing](documentation/testing/payment_4.png)

  - Filled out the payment form and clicked on the submit button:

    ![Django unit testing. Payment. Coverage. Missing](documentation/testing/payment_5.png)

  - In the terminal, I was able to see that the stock is updated and the order is created

    ![Django unit testing. Payment. Coverage. Missing](documentation/testing/payment_2.png)

  - In the admin panel, I was able to see that the order is created and the billing status is set to True, which proves that the webhook is working correctly.

    ![Django unit testing. Payment. Coverage. Missing](documentation/testing/webhooks_work.png)

## Bugs

**Solved bugs:**
1. I was getting an error message when I tried to test the JsonResponse response on Password change.

*Solution:*

Added `request.user` argument to the `PasswordChangeForm` form.

```python
    password_form = PasswordChangeForm(request.user, request.POST)
```

2. I was logged out right after the user logged in and the tests were showing the error `The view profiles.views.EditUserProfileView didn't return an HttpResponse object. It returned None instead.`

*Solution:*

Add additional import to the profiles views: `update_session_auth_hash`
And after saving the form, call the `update_session_auth_hash` function:

```python
    from django.contrib.auth import update_session_auth_hash

    if password_form.is_valid():
    password_form.save()
    update_session_auth_hash(request, password_form.user)
    return JsonResponse({'success': True})
```
3. I was struggling to get countries, county/regions, cities using various libraries. When planning the project I was aimed to use the `django-cities-light` library but this library is very heavy, and therefore, I wouldn't be able to deploy it to Heroku for free. Thus, I decided to use the [geonames](https://www.geonames.org/). The first issue that I encountered was that the link to the geonames website was not working. It was simply solved be enabling my account to use the geonames website. The following issue was regarding the selection regions and cities.

*Solution:*

Rather than searching for the regions by country name/code, I used country id to search for the regions.

```javascript
    let countryId = $('#id_country').find(':selected').data('id');
```

After retrieving the regions, I was able to get the first word of the region name and use it to search for the cities by link:

```javascript
    let stateName = $('#id_county_region').find(':selected').text();
    let stateNameFirstWord = stateName.split(' ')[0];
```

and url for AJAX request:

```javascript
    url: 'https://secure.geonames.org/searchJSON?q=' + stateNameFirstWord + '&username=<my_account_name>&style=FULL&fclName=city, village,...&maxRows=1000',
```

4. I was trying to get cover image for the product using related_name and if statements in the template. However, I was not able to get a single image, which is whether default and active, or not default but the first in the list of active images (```{% if forloop.first %}```).

*Solution:*

I added a method to the Product model that allows me to get the cover image.

```python
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
            return 'static/images/default_product_image.png' 
        else:
            return 'static/images/default_product_image.png' 
```

5. I realized that my .gitiignore file was not ignoring the db.sqlite3 file, however, it was stating the .gitiignore file 
```python
    *.sqlite3
    db.sqlite3
```

*Solution:*

At the very beginning, I used the following command:

```
git update-index --assume-unchanged db.sqlite3
```

But the output was: ```fatal: Unable to mark file db.sqlite3```

So, I user the following command for reset:

```
git reset HEAD
```
After that I run assume-unchanged again:

```
git update-index --assume-unchanged db.sqlite3
```

6. I was trying to create signals to create Stock when a ProductInventory is created.
However, I failed since I was using save method in the Stock model, which checks if there are any Product Inventory units available (if there 0 units, it will set ProductInventory.is_available to False). At first, I was trying to create a save method in the ProductInventory model to recreate signals, but I was not able to as it was calling "Unique constraint" error.

*Solution:*

I implemented checking functionality in views.py to prevent any errors:

```python
    product_inventory_active_stock = Stock.objects.filter(
                product_inventory=product_inventory_active
            )
            if product_inventory_active_stock:
                # do something
```

7. During the development of the bag functionality, I have noticed that js code was sending not the correct id data.

*Solution:*

I created product_inventory_id variable outside of the functions and reassigned it to the id of the ProductInventory object, which was checked in on change event.

```javascript
  let product_inventory_id = 0
    $('.product__options').on('change', 'input', function() {
      let attribute_value = $(this).val();
      let attribute_name = $(this).get(0).name;
      let availableAttrsFromOtherGroups = [];
      for (let stockOption of values_list_array) {
        if (stockOption[attribute_name] == attribute_value && stockOption["Quantity"] > 0) {
          for(let key in stockOption) {
            if (key != "Quantity" && key != attribute_name) {
              if (key == "id") {
                product_inventory_id = stockOption[key];
              }
              availableAttrsFromOtherGroups.push(stockOption[key]);
            }
          }
        }
      }
    });
```

8. When I was trying to implement sending email on successful payment with url link functionality, I was receiving only content_html in the email without the content_text.

![Payment confirmation email bug](documentation/bugs/payment_confirmation_bug.png)

  *Solution:* Move the email content into email content template.

![Payment confirmation email bug solution](documentation/bugs/payment_confirmation_email_solution.png)


```python
from django.core.mail import EmailMultiAlternatives


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)
    # send email to the customer
    order = Order.objects.get(order_key=data)
    # get this order
    order_id = order.id   
    order_obj = Order.objects.get(id=order_id)
    customer = order_obj.user
    subject = 'Payment Confirmation'
    # get the order total paid
    order_total_paid = order_obj.total_paid
    order_num = str(order_obj.order_number)
    link = (
        'https://wowder.herokuapp.com/orders/' + str(customer.username) +
        '/my_orders/' + order_num + '/'
    )
    subject, from_email, to = (
        'Payment Confirmation', 'wow@der.com', str(customer.email)
    )
    text_content = ''
    html_content = '<h1>Payment Confirmation</h2>' \
                '<p>Your payment of ' + str(order_total_paid) \
                + ' has been confirmed.</p>' \
                '<p>You can view your order details by ' \
                'clicking on your your order information link below:</p>' \
                '<strong>Order ID: </strong>' \
                '<a href=' + link + '>' + order_num + \
                '</a><br><p>Thank you for shopping with us!</p>' \
                '<em>WoWder shop</em>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)

```

9. After adding values for men and women sizing, I got an error of returning more than 1 object on get method. I t was due to the same values for sizing, like L size for men clothing and L size for women clothing

*Solution:* Change get method on filter and adding for loop to go through all received objects:

```python
    attribute_testing_set_list = list(attribute_testing_set)
    selected_value = ProductAttributeValue.objects.filter(
        attribute_value=value.attributevalues
    )
    for s_v in selected_value:
        for attribute in attribute_testing_set_list:
            # Check if the attribute is in the attr set list
            if str(attribute) == str(
                s_v.product_attribute
            ):
                product_inventory_active_values[
                    attribute
                ] = s_v.attribute_value
```


## Validation

### HTML Validation:
- No errors or warnings were found when passing through the official [W3C](https://validator.w3.org/) validator. This checking was done manually by copying the view page source code (Ctrl+U) and pasting it into the validator.

- [Bag app HTML validation report](documentation/validation/bag_html_validation.pdf)

- [EmailNotification app HTML validation report](documentation/validation/email_notification_html_validation.pdf)

- [Home app HTML validation report](documentation/validation/home_html_validation.pdf)

- [Inventory app HTML validation report](documentation/validation/inventory_html_validation.pdf)

- [Orders app HTML validation report](documentation/validation/orders_html_validation.pdf)

- [Payment app HTML validation report](documentation/validation/payment_html_validation.pdf)




### Python Validation:

- No errors were found when the code was passed through Valentin Bryukhanov's [online validation tool](http://pep8online.com/). According to the reports, the code is [Pep 8-compliant](https://legacy.python.org/dev/peps/pep-0008/). This checking was done manually by copying python code and pasting it into the validator.

#### Bag app

[Bag. Validation Report](documentation/validation/pep8_validation_bag.pdf)

#### Email_notifications app

[Email_notifications. Validation Report](documentation/validation/pep8_validation_email_notifications.pdf)

#### Home app

[Home. Validation Report](documentation/validation/pep8_validation_home.pdf)

#### Inventory app

[Inventory. Validation Report](documentation/validation/pep8_validation_inventory.pdf)

#### Orders app

[Orders. Validation Report](documentation/validation/pep8_validation_orders.pdf)

#### Payment app

[Payment. Validation Report](documentation/validation/pep8_validation_payment.pdf)

#### Personnel app

[Personnel. Validation Report](documentation/validation/pep8_validation_personnel.pdf)

#### Profiles app

[Profiles. Validation Report](documentation/validation/pep8_validation_profiles.pdf)

#### Promotions app

[Promotions. Validation Report](documentation/validation/pep8_validation_promotions.pdf)

#### Reviews app

[Reviews. Validation Report](documentation/validation/pep8_validation_reviews.pdf)

#### Wishlist app

[Wishlist. Validation report](documentation/validation/pep8_validation_wishlist.pdf)

#### Errors:

The errors were made in the following commits:

1. 3cb0b4f275e0650749c9f5cee59072d3889e4a97

Aff wishlist app and url path - > Add instead of Aff

2. da08e5f77a1f886ba7e492d0f2c4aaf20782f5cb

Add url path for viewing product - > Add test for url path

3. a13d44771be873e84c8f60750efe12b5b4ff5d89

Add ProductInventoriesTable View - > Add product_inventory_table url path

4. 55748cb415b51a625a38d04a68b3e2db7d6caab0

Ad categories data to template - > Add categories data to template

5. ec5a9ae366c8cd077c2d3d45e9e308b912b49c5d

Add view for adding brand functionality -> Add testing to test adding brand functionality

6. 64d3e92baacd3f271da0a36bcaebcac2cf5be6e5

Add edit_order_item_url -> Add tests for edit order item functionality

7. bd39e0881a6734c017728011b0020f32ba46ce60

Add custom stylings for search buttons -> Change if condition to show all categories products

8. 9091743069373eefd32a46b1365389860fce14e6

Add functions handlers for 400 and 505 errors - > Add functions handlers for 404 and 500 errors