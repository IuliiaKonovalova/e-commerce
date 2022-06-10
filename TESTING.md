# TESTING

## Automated testing

### Django unit testing

**Solved issues:**

1. I couldn't figure out how to test save methods in Address model as I was receiving the correct result in my print statements in the terminal but at the same time I was getting an error message.

![Calling save() for Address Model](documentation/testing/tests_issues1.png)

*Solution*:

rather than calling ```self.assertEqual(self.address2.is_primary, True)```, I created a separate variable for the ```address2``` and called it:

```python
  address2 = Address.objects.get(id=2)
  self.assertEqual(address2.is_primary, False)
```

![Calling save() for Address Model. Solution](documentation/testing/tests_issues2.png)

**Unsolved issues:**

1. I was getting an error message when I tried multiple times to test JsonResponse response on Password change.

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
