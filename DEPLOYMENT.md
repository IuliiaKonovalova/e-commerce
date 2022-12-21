# Deployment and Payment setup

- The app was deployed to [Render](https://render.com/).
- The database was deployed to [ElephantSQL](https://www.elephantsql.com/).

- The app can be reached by the [link](https://wowder.onrender.com).

---

## Payment Setup

1. Register a stripe account at https://dashboard.stripe.com/register.
2. Go to the developers' page:

![developers](documentation/payment_setup/developers__btn.png)

3. Select API keys.

![api_keys](documentation/payment_setup/api_keys.png)

4. Copy the `public key` and `secret key` to the `env.py` file.

5. Add the following setting to `settings.py`:

```python
  STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
  STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
```

6. Install stripe package:

```python
  pip3 install stripe
```

7. Create an order model with the required fields in the orders app.
8. Set up a payment app.
9. Add a payment form to the payment app template.
10. Add div to hold stripe element:

```html
  <div id="stripe-element"></div>
```
11. Create a View to handle payment setup:
  - Get public key: `stripe_public_key = settings.STRIPE_PUBLIC_KEY`
  - Get private key: `stripe_secret_key = settings.STRIPE_SECRET_KEY`
  - create intent: `intent = stripe.PaymentIntent.create(**kwargs)`
  - **kwargs for the payment intent should include:
    * `amount`: amount
    * `currency`: currency
    * `metadata`: metadata
  - For the metadata, I have user id `userid: request.user.id`
  - Create context for the view with the following data:
      *  'my_profile': my_profile,
      *  'total_sum': total_sum,
      *  'client_secret': intent.client_secret,
      *  'stripe_public_key': stripe_public_key,

12. Add extra js block to payment template where you have to add csrf_token, stripe_public_key,
  script tag with stripe.js, and script tag with payment.js.

```html
  {% block postloadjs_extra %}
    <script>
        let CSRF_TOKEN = '{{ csrf_token }}';
        let stripe_public_key = '{{ stripe_public_key }}';
    </script>
    <script src="https://js.stripe.com/v3/"></script>
    <script src="{% static 'js/payment.js' %}" data-rel-js></script>
  {% endblock %}
```

13. In the payment.js, create variables for stripe public key, stripe, payment element, payment form, and a variable from which you will receive 'client_secret.' To get 'client secret,` I have added data-attribute to confirmation button in the payment form:

```html
  data-secret="{{ client_secret }}"
```
14. Set up stripe element:

```javascript
  let elements = stripe.elements();
  let style = {
    base: {
      color: "#000",
      lineHeight: '2.4',
      fontSize: '16px'
    }
  };
  let card = elements.create("card", {
    style: style
  });
  card.mount("#card-element");
```

*You can use various styling by checking out the following docs [stripe/elements-examples](https://github.com/stripe/elements-examples)*

15. Get all data from the payment form and collect it by using `new FormData()`

16. Create an AJAX request to send collected data and set the url to for adding order. The URL is `window.location.origin + '/orders/add/'`.

17. In the orders app views, you need to create a view to handle order creation.

18. The payment intent is created when the user clicks on the confirmation button. That stripe element prevents the user from multiple clicks and handles all errors. However, you must set alerts for the user to show the error.

19. To test the user's payment, you need to create a test payment intent with the card data provided by the stripe:

No auth: 4242424242424242

Auth: 4000002500003155

Error: 4000000000009995

20. Create a success page to redirect the user after successful payment and add js functionality to handle the redirection:

```javascript
    if (result.paymentIntent.status === 'succeeded') {
      window.location.replace(window.location.origin + "/payment/order_placed/");
    }
```

21. Set app stripe backend:
  - Go to [Stripe Docs. Stripe CLI](https://stripe.com/docs/stripe-cli)
  - Download the stripe-cli file depending on your operating system.

  ![stripe-cli](documentation/payment_setup/stripe_cli_docs.png)

  - In my case, I downloaded the file for Linux:

  ![stripe-cli](documentation/payment_setup/stripe_cli_docs_linux.png)

  - Go to the link provided and download the file.

  ![stripe-cli](documentation/payment_setup/stipe_linux_x86_64.png)

  - Open the downloaded file and move the file `stripe` to the project's root directory.

  - Open the terminal and type:

  `./stripe login`

  *Note! For the window OS, the command looks as follows `stripe login`*

  - Hit enter -> You will be redirected to the Stripe dashboard, where you need to allow access to your local workspace.

  - Create a payment, and the intent will be created.

  *Another option:*
  
  - Download the following file:

  ![stripe-cli](documentation/payment_setup/stripe_directly.png)

  - Open the downloads folder in the terminal and type:

  `sudo gdebi stripe_1.11.0_linux_amd64.deb`

  - The package will be installed -> Type `stripe` in the terminal and hit enter.

22. Create a function in the orders views to handle the payment confirmation, which will take payment data. This function will also handle email confirmation.

23. To run this function, you will need to add the following process provided by stripe:

```python
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
  def stripe_webhook(request):
      payload = request.body
      event = None
      try:
          event = stripe.Event.construct_from(
              json.loads(payload), stripe.api_key
          )
      except ValueError as e:
          return HttpResponse(status=400)
      # Handle the event
      if event.type == 'payment_intent.succeeded':
          payment_confirmation(event.data.object.client_secret)
      else:
          print('Unhandled event type {}'.format(event.type))
      return HttpResponse(status=200)
```

24. Add URL to the stripe_webhook function in the payment urls.py

```python
    path('webhook/', stripe_webhook),
```

25. In the terminal type:

`./stripe listen --forward-to localhost:8000/payment/webhook/`

26. Remember to set app stripe data in Heroku configs:

  - Create a webhook in the stripe dashboard and set the hosted endpoint.

  ![webhook](documentation/payment_setup/stripe_webhook.png)

  - `STRIPE_PUBLIC_KEY`
  - `STRIPE_SECRET_KEY`
  - `STRIPE_WEBHOOK_SECRET`

---

## Local deployment

1. Clone the repository.

    - ```git clone https://github.com/IuliiaKonovalova/e-commerce.git```

2. Go to the ```ecommerce_project``` directory.

    - ```cd ecommerce_project```

3. Create a virtual environment.

    - ```python3 -m venv venv```

    - ```source venv/bin/activate```

4. Install all dependencies.

    - ```pip install -r requirements.txt```

5. Create a ```env.py``` file.

    - ```touch env.py```

6. Add the following lines to ```env.py```:

    - ```import os```
    - ```os.environ["SECRET_KEY"]``` = your secret key.
    - ```os.environ["DEBUG"]``` = "True" or "False" depending on whether you are in development or production.
    - ```os.environ["DEVELOPMENT"]``` = "True" or "False" depending on whether you are in development or production.
    - ```os.environ["ALLOWED_HOSTS"]``` = your domain name.
    - ```os.environ["DATABASE_URL"]``` = your database url.
    - ```os.environ["CLOUDINARY_CLOUD_NAME"]``` = your cloudinary cloud name.
    - ```os.environ["CLOUDINARY_API_KEY"]``` = your cloudinary api key.
    - ```os.environ["CLOUDINARY_API_SECRET"]``` = your cloudinary api secret.
    - ```os.environ["STRIPE_PUBLIC_KEY"]``` = your stripe public key.
    - ```os.environ["STRIPE_SECRET_KEY"]``` = your stripe secret key.
    - ```os.environ["STRIPE_WEBHOOK_SECRET"]``` = your stripe webhook secret key.

7. Create and migrate the database.

---

## Important note


**NOTE !**

As the app requires assigning a role for each user, you will need to apply some changes Profile model for the role field.:

```python
    class Profile(models.Model):
        """Model for the profiles."""
        user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name='profile',
            verbose_name='User',
            help_text=(
                'format: required, unique=True'
            )
        )
        first_name = models.CharField(
            max_length=50,
            blank=True,
            null=True,
            verbose_name='First name',
            help_text=(
                'format: not required, max_length=50'
            )
        )
        last_name = models.CharField(
            max_length=50,
            blank=True,
            null=True,
            verbose_name='Last name',
            help_text=(
                'format: not required, max_length=50'
            )
        )
        birthday = models.DateField(
            blank=True,
            null=True,
            verbose_name='Birthday',
            help_text=(
                'format: not required'
            )
        )
        avatar = CloudinaryField(
            'avatar',
            folder='avatars',
            blank=True,
            null=True,
        )
        subscription = models.BooleanField(
            default=False,
            verbose_name='Subscription',
            help_text=(
                'format: not required'
            )
        )
        role = models.ForeignKey(
            Role,
            on_delete=models.SET_NULL,
            null=True,
            # default=1, # 1 is the default role that should be commented out before the first migrations
            verbose_name='Role',
            help_text=(
                'format: not required'
            )
        )
        created_at = models.DateTimeField(
            auto_now_add=True,
            verbose_name='Created at',
        )
        updated_at = models.DateTimeField(
            auto_now=True,
            verbose_name='Updated at',
        )
```

- ```python manage.py makemigrations```
- ```python manage.py migrate```

- After migration, you will need to create a superuser.


8. Create the superuser.

    - ```python manage.py createsuperuser```

9. Create roles as following:

For example:

```python
    Role.objects.create(name='Customer')
    Role.objects.create(name='Manager')
    Role.objects.create(name='Admin')
```


10. Set the role for the superuser with the role field with id 3.

```python
    superuser.profile.role_id = 3
    superuser.save()
```

11. Go to Profiles and uncomment the default role. Make new migrations and migrate.

    - ```python manage.py makemigrations```
    - ```python manage.py migrate```

**After the following steps, you will ensure that the app is working correctly, and any other user registered in your app will only have access as a customer. The rest of the roles will be controlled by the admin.**


12. Run the server.

    - ```python manage.py runserver```

13. Access the website by the link provided in terminal. Add ```/admin/``` at the end of the link to access the admin panel.


*If you are using Gitpod, you can skip steps 1-3 by clicking this [link](https://gitpod.io/#https://github.com/IuliiaKonovalova/e-commerce), and start from step 4.*

---
