# Features


## Access to pages according to the user role:

| Page Name | Logged out  | Customers  | Manager | Admin |
| --------- | ----------- | ---------- | ------- | ----- |
| Home       | Yes         | Yes        | Yes     | Yes   |
| Login      | Yes         | Yes        | Yes     | Yes   |
| Register   | Yes         | Yes        | Yes     | Yes   |
| Logout     | Yes         | Yes        | Yes     | Yes   |
| Store Products   | Yes         | Yes        | Yes     | Yes   |
| Store Product's Details | Yes         | Yes        | Yes     | Yes   |
| All reviews   | Yes         | Yes        | Yes     | Yes   |
| Bag       | No         | Yes        | Yes     | Yes   |
| Profile   | No         | Yes        | Yes     | Yes   |
| Edit profile   | No         | Yes        | Yes     | Yes   |
| Add address   | No         | Yes        | Yes     | Yes   |
| All addresses   | No         | Yes        | Yes     | Yes   |
| Edit address   | No         | Yes        | Yes     | Yes   |
| My Orders   | No         | Yes        | Yes     | Yes   |
| My Order's Details   | No         | Yes        | Yes     | Yes   |
| My Wishlist   | No         | Yes        | Yes     | Yes   |
| My reviews   | No         | Yes        | Yes     | Yes   |
| My reviews' Details   | No         | Yes        | Yes     | Yes   |
| Checkout   | No         | Yes        | Yes     | Yes   |
| Promotions | No         | No         | Yes     | Yes   |
| Add promotion | No         | No         | No     | Yes   |
| Edit promotion | No         | No         | No     | Yes   |
| Delete promotion | No         | No         | No     | Yes   |
| Create newsletter-promo Email | No         | No         | Yes     | Yes   |
| Categories | No         | No         | Yes     | Yes   |
| Add category | No         | No         | Yes     | Yes   |
| Edit category | No         | No         | Yes     | Yes   |
| Delete category | No         | No         | No     | Yes   |
| Brands | No         | No         | Yes     | Yes   |
| Brand's details | No         | No         | Yes     | Yes   |
| Edit brand | No         | No         | Yes     | Yes   |
| Delete brand | No         | No         | No     | Yes   |
| Tags | No         | No         | Yes     | Yes   |
| Add tag | No         | No         | Yes     | Yes   |
| Edit tag | No         | No         | Yes     | Yes   |
| Delete tag | No         | No         | Yes     | Yes   |
| Products' Types | No         | No         | Yes     | Yes   |
| Add product's type | No         | No         | Yes     | Yes   |
| Edit product's type | No         | No         | Yes     | Yes   |
| Delete product's type | No         | No         | No     | Yes   |
| Products' attributes | No         | No         | Yes     | Yes   |
| Add product's attribute | No         | No         | Yes     | Yes   |
| Edit product's attribute | No         | No         | Yes     | Yes   |
| Delete product's attribute | No         | No         | No     | Yes   |
| Product's values | No         | No         | Yes     | Yes   |
| Add product's value | No         | No         | Yes     | Yes   |
| Edit product's value | No         | No         | Yes     | Yes   |
| Delete product's value | No         | No         | No     | Yes   |
| Personnel Products Table | No         | No         | Yes     | Yes   |
| Add product | No         | No         | Yes     | Yes   |
| Edit product | No         | No         | Yes     | Yes   |
| Delete product | No         | No         | Yes     | Yes   |
| Personnel Product's full details | No         | No         | Yes     | Yes   |
| Add new image modal | No         | No         | Yes     | Yes   |
| Edit image modal | No         | No         | Yes     | Yes   |
| Delete image modal | No         | No         | Yes     | Yes   |
| Add product's unit | No         | No         | Yes     | Yes   |
| Edit product's unit | No         | No         | Yes     | Yes   |
| Delete product's unit | No         | No         | Yes     | Yes   |
| Product's units | No         | No         | Yes     | Yes   |
| Product's unit's details | No         | No         | Yes     | Yes   |
| Add stock | No         | No         | No     | Yes   |
| Edit stock | No         | No         | No     | Yes   |
| Delete stock | No         | No         | No     | Yes   |
| Stock table | No         | No         | No     | Yes   |
| Orders | No         | No         | Yes     | Yes   |
| Order's details | No         | No         | Yes     | Yes   |
| Edit order status feature | No         | No         | No     | Yes + Logistics manager   |
| Edit Order | No         | No         | No     | Yes   |
| Delete order | No         | No         | No     | Yes   |
| Edit order's item | No         | No         | No     | Yes   |
| Delete order's item | No         | No         | No     | Yes   |


## Main Features:

- Each page has a navbar and a footer

### Navbar:

Navbar has 2 subsections:

1. Customer's section, which is visible for all users:

    - if the user is logged in, the navbar has the following features:

      ![Navbar](documentation/features/navbar/navbar_customer.png)
      
        - logo, which redirects to the home page;
        
        ![Logo](documentation/features/navbar/navbar_logo.png)
        
        - Store button, which redirects the user to the store page

        - Wishlist button, which redirects the user to the wishlist page

        - Bag button, which redirects the user to the bag page

        - Profile button, which redirects the user to the profile page

        - Logout button, which redirects the user to the login page


    - if the user is logged out, the navbar has the following features:
    
      ![Navbar](documentation/features/navbar/navbar_logged_out.png)
      
        - logo:
        
        ![Logo](documentation/features/navbar/navbar_logo.png)
        
        - It has only Store, Wishlist and Bag buttons, which redirects the user to the store page, wishlist page and bag page respectively.

        - Login button, which redirects the user to the login page

        - SignUp button, which redirects the user to the register page

2. Personnel's section, which is visible only for store personnel:
      
      ![Navbar. Personnel](documentation/features/navbar/navbar_personnel.png)

    It has Personnel's button, which is visible only for store personnel. When this buttons is clicked, the user will see a dropdown menu with following navbar features:

    ![Navbar. Personnel. Dropdown](documentation/features/navbar/navbar_personnel_dropdown.png)

    - Promo button, which redirects the user to the promotions page

    - Email button, which redirects the user to the create newsletter or promotional email page;

    - Categories button, which redirects the user to the categories page;

    - Brands button, which redirects the user to the brands page;

    - Tags button, which redirects the user to the tags page;

    - Products' Types button, which redirects the user to the products' types page;

    - Products' Attributes button, which redirects the user to the products' attributes page;

    - Products' Values button, which redirects the user to the products' values page;

    - Personnel Products Table button, which redirects the user to the personnel products table page;

    - Units button, which redirects the user to the units table page;

    - Stock button, which redirects the user to the stock table page;

    - Orders button, which redirects the user to the orders page;

    - Stock requests button, which redirects the user to the stock requests page;

The simplistic design of the navbar is based on the decision to make the use of the webapp easy for the all users.

*Navbar is slightly different on the tablet devices*

![Navbar. Tablets](documentation/features/navbar/navbar_tablets.png)

*Navbar looks as following on the mobile devices*

![Navbar. Mobiles](documentation/features/navbar/navbar_mobile.png)

### Footer:

![Footer](documentation/features/footer/footer.png)

Footer has the following features:

- logo;

- contact information;

- About us button, which redirects the home page;

- Jobs button, which redirects the Linkedin page (the implementation is necessary for the future);

- Products button, which redirects the store page;

- Contact us button, which allows the user to send an email to the store personnel;

- Privacy Policy button, which redirects the privacy policy page;

- Social media buttons: instagram, facebook, twitter (the implementation is necessary for the future);

- And the information about the creator of the webapp with the link to github.

*Footer is slightly different on the mobile devices*

![Footer. Mobile](documentation/features/footer/footer_mobile.png)

### Home page:

![Home page](documentation/features/home/home_page.png)

Home page has:

- Hero section:

![Hero section. Hero Section](documentation/features/home/home_hero_section.png)

This section has a logo in the left top corner. There is also a eye-catching image on the right side of hero section.
Underneath the logo is a description of the store and button. If user is logged in, the button has the following text "Start Shopping", which redirects the user to the store page.
If user is logged out, the button has the following text "Get Started", which redirects the user to the SignUp page.

![Hero section. Hero section. User logged out](documentation/features/home/home_hero_section_user_logged_out.png)

- About Us section:

![About Us section. Part 1](documentation/features/home/about_us_section_1.png)

![About Us section. Part 2](documentation/features/home/about_section_2.png)

This section describes the benefits of being a customer of the store, such as "The best quality", "The best prices", "Your privacy is our priority", "Fast delivery", and "Being in touch".

- Testimonials section:

![Testimonials section](documentation/features/home/testimonials_section.png)

This section presents the testimonials of the store customers and aimed at giving the user an idea of the quality of the store.

*Home page is slightly different on the mobile devices*

![Home page. Mobile](documentation/features/home/home_page_mobile.png)

### My profile page:

![My profile page](documentation/features/my_profile/my_profile_page.png)

This page has the main data on the customer for the logged in user.

- It has avatar, full name, primary address (if it is set), profile navigation:

![My profile Card](documentation/features/my_profile/my_profile_card.png)

- Profile navigation has the following buttons:

  - Edit profile button, which redirects the user to the edit profile page;

  - My addresses button, which redirects the user to the my addresses page; (*If user hasn't added any addresses, the button will say: add address, and the user will be redirected to add address page*)

  - My orders button, which redirects the user to the my orders page;

  - My wishlist button, which redirects the user to the my wishlist page;

  - My reviews button, which redirects the user to the my reviews page;

### Edit Profile page:

![Edit Profile page](documentation/features/edit_profile/edit_profile_page.png)

This page has the main data on the customer for the logged in user and allows user to edit this data.

It has four forms:

  - Edit avatar form;

    ![Edit avatar form](documentation/features/edit_profile/edit_avatar_form.png)

    - if user wants to upload an avatar, he can do it by clicking the "Edit" button, and the user will be able to select an image from his computer. When the user selects and image, the form will be filled with the image's data:

    ![Edit avatar form. Image selected](documentation/features/edit_profile/edit_avatar_new.png)

  - Edit Profile Data Form;
  
    ![Edit Profile Data Form](documentation/features/edit_profile/edit_profile_data_form.png)
    
  - Change Password Form;
  
    ![Change Password Form](documentation/features/edit_profile/change_password_form.png)

  - Delete Account Form;

    ![Delete Account Form](documentation/features/edit_profile/delete_account_form.png)

    - If the user clicks the "Delete" button, the user will be asked to confirm the deletion.

    ![Delete Account Form. Confirmation](documentation/features/edit_profile/delete_profile_form_dropdown.png)

    - If user confirms the deletion, the user will be redirected to the home page.

    - If user doesn't confirm the deletion, the delete account form will be closed.

### My addresses page:

![My addresses page](documentation/features/my_addresses/my_addresses_page.png)

This page empowers customers to store their addresses. And easily allows them to edit and delete them as well as set the primary address.

It has a button: "Add new address", which redirects the user to the add address page.

![My addresses page. Add new address button](documentation/features/my_addresses/add_new_address_button.png)

It has table of address's cards:

Only one address can be primary.

Each card has address data and 2 buttons.

  - Edit button, which redirects the user to the edit address page;
  
  - Primary address card has also a "Disable as Primary" button, which allows the user to disable the primary address.

![My addresses page. Table](documentation/features/my_addresses/address_card_primary.png)

The primary address card is distinguished by the "Primary" label and purple background.

  - Not primary address card has also a "Enable as Primary" button, which allows the user to make the address primary, and disable the previous primary address.

![My addresses page. Table. Not primary address card](documentation/features/my_addresses/address_card_not_primary.png)


### Add address page:

![Add address page](documentation/features/add_address/add_new_address_form.png)

This page allows the user to add a new address by selecting the country, state, city, and typing the address, zip code, and phone number. The user can also select the address as primary.

![Add address page. Primary address](documentation/features/add_address/address_form_dropdown.png)

It also has 2 buttons:

  - Save address button, which redirects the user to the my addresses page and saves the address;
  
  - Cancel button, which redirects the user to the my addresses page.

### Edit address page:

![Edit address page](documentation/features/edit_address/edit_address_form.png)

This form has the same fields as the add address form. However, it has prefilled data on the address.

I has 2 buttons:

  - Save address button, which redirects the user to the my addresses page and saves changes to the address;
  
  - Cancel button, which redirects the user to the my addresses page.

**Under the edit address page, the user can find delete address button**

If user clicks the delete address button, the user will be asked to confirm the deletion.

![Edit address page. Confirmation](documentation/features/edit_address/delete_address.png)

- If user confirms the deletion, the user will be redirected to the my addresses page.

- If user doesn't confirm the deletion, the delete address form will be closed.

### My orders page:

![My orders page](documentation/features/my_orders/my_orders_page.png)

This page has a full data on the customer's orders and presented by orders' cards.

![My orders page. Table](documentation/features/my_orders/orders_cards.png)

Each card has a short description of the order, the date of the order, the total price of the order, and the status of the order.

If the user clicks on the order card, the user will be redirected to the order detail page.

### My Order detail page:

![My Order detail page](documentation/features/my_order_details/my_order_detail_page.png)

This page has an store order number as a title and "Back to my orders" button, which redirects the user to the my orders page. 

![My Order detail page. Title. Button](documentation/features/my_order_details/my_order_detail_title_button.png)

Under the title, the user can find the order's data shown as a table:

1. Order summary:

![My Order detail page. Table. Order summary](documentation/features/my_order_details/my_order_detail_data.png)

2. Order items:

![My Order detail page. Table. Order items](documentation/features/my_order_details/my_order_detail_item.png)

For each item, the user can find the product's name with the link to the product in store, quantity, price, and total price. If user clicks on the product's name or product's image, the user will be redirected to the product detail page.

**If order is completed, Customer is allowed to add reviews on the products**

![My Order detail page. Table. Order items. Reviews](documentation/features/my_order_details/my_order_details_completed_order.png)

Each item got the same button: "Add review".

If user clicks on the button, the user will be redirected to the add review page.

If user has already added a review, the button be "View review".

![My Order detail page. Table. Order items. Reviews. Button](documentation/features/my_order_details/order_details_view_review.png)

If user forgot to close the window with the add review page, and review has already been added, the user will be redirected to the review already added page.

![My Order detail page. Table. Order items. Reviews. Button. Review already added](documentation/features/my_order_details/order_details_review_already_added.png)


### Add review page:

![Add review page](documentation/features/add_review/add_review_page.png)

This page has a form to add a review.

1. Rating:

![Add review page. Rating](documentation/features/add_review/add_review_rating.png)

Where user can select the rating.

2. Comment:

Where user can type the comment.

3. Images:

  - If user has uploaded images, they will be shown in the form;
  
  - If user has not uploaded images, they will be shown in the form.

![Add review page. Images](documentation/features/add_review/add_review_images.png)

4. Form control buttons:

  - Save review button, which redirects the user to the my order detail page and saves the review;
  
  - Cancel button, which redirects the user to the my order detail page.


### All reviews page:

![All reviews page](documentation/features/my_reviews/all_my_reviews.png)

This page has all reviews that the user has left. It presented by reviews' cards. If user clicks on the review card, the user will be redirected to the review detail page.


### My review page:

![My reviews page](documentation/features/my_review/my_reviews_page.png)

This page has oll data on the review left by the user.

**However, the edition of the review is not allowed**

![My reviews page. Table](documentation/features/my_review/my_review_details_alert_msg.png)

This decision was made based on the fact that the shop owner has to evaluate all aspects of the customer's experience: product quality, delivery speed, and customer service.

It has been made to prevent the user from editing the review with no reason.

This trend is highly appreciated by Chinese online shopping community.


### Store page:

![Store page](documentation/features/store/store_page.png)

This page has the following features:

  - Search-select bar:

    ![Search-select bar](documentation/features/store/store_search_bar.png)

    - Search bar:

    User can simply type the name of the product in the search bar and the system will show the products that match the search.

    ![Search bar](documentation/features/store/search_tomatoes.png)

    - Select bar:

    User can select the category of the product in the select bar and the system will show the products that match the category.

    ![Select bar](documentation/features/store/sort_by_category.png)

  - Products:

    User can see the products that are in the store. The products are displayed in a grid with the following features:
    
    **Product card:**

    ![Products. Product Card](documentation/features/store/store_product_card.png)

    It has the main image of the product, the name of the product, the price of the product, the button "Add to wishlist", and special labels. If the product in new, the label "New" is displayed. If the product is on sale, the label "Sale" is displayed.

    If the user didn't like the product, the button outline heart is displayed. If the user likes the product, the button filled heart is displayed. And etc.

    ![Products. Product Card. Liked](documentation/features/store/store_product_card_liked.png)

    The spin icon is displayed when the user call is processing the request.

    ![Products. Product Card. Spinner](documentation/features/store/store_product_card_processing.png)

    Special features of the product card:

    The price of products can be different depending on the product's values. For example, if the product has a value "Size", the price of the product can be different depending on the size of the product. If the product out of stock, the price is displayed as "Out of stock".

    ![Products. Product Card. Prices variation](documentation/features/store/store_products_cards_prices.png)

  - Pages:

    ![Pages](documentation/features/store/store_page_navigation.png)

### Product's details page:

![Product's details page](documentation/features/product_details/product_details_page.png)

This page has the product's card with full data.

The left side of the products card has the following features:

![Product's details page. Left side of the card](documentation/features/product_details/product_details_left.png)

It has the main image of the product with carousel. When the user clicks on the left or right arrow, the carousel will change the image.

  ![Product's details page. carousel 1](documentation/features/product_details/carousel1.png)
  ![Product's details page. carousel 2](documentation/features/product_details/carousel2.png)
  ![Product's details page. carousel 3](documentation/features/product_details/carousel3.png)

It also has labels:

  - if product is on sale, the label "Sale" is displayed;

  - if product is new, the label "New" is displayed;

Underneath the main image of the product is the "Add to wishlist" section. When the user clicks on the outline heart button, the product is added to the wishlist.

And the message will appear in the top right corner of the page:

![Product's details page. Add to wishlist msg success](documentation/features/product_details/add_to_wishlist_msg.png)

And the heart icon button will turn to be filled heart button.

![Product's details page. Liked](documentation/features/product_details/added_to_wishlist.png)

*While the request is processing, the spin icon is displayed*

![Product's details page. Liked Spinner](documentation/features/product_details/adding_to_wishlist.png)

Under this section the user may find the reviews of the product and overall rating of the product.

![Product's details page. Reviews section](documentation/features/product_details/product_rating_reviews.png)

When the user clicks "View reviews", the user will be redirected to the product's reviews page.

The right side of the product card has the following features:

  ![Product's details page. Right side of the card](documentation/features/product_details/product_details_right.png)

  *"Add to bag button will be disable if there are any options which are specified by the customer.**

  ![Product's details page. Add to bag disable](documentation/features/product_details/add_to_bag_diable.png)

  - Product's full name;
  
  - Product's description;

  - Reset button, which allows the user to reset the values of the product;

    ![Product's details page. Reset button](documentation/features/product_details/product_option_reset_button.png)

  - Product's options' section:
  
    ![Product's details page. Products values](documentation/features/product_details/product_options.png)

    - User can select the value of the product's option.

    *If the options are chosen, the "Add to bag" button will be enabled.*

    ![Product's details page. Add to bag enable](documentation/features/product_details/add_to_bag_enable.png)

    If options have colors, the user can see the example of the color right away.

    - if the product has no options, the section is not displayed;

    ![Product's details page. Product without options](documentation/features/product_details/product_no_options.png)

    *If there are no options at all for a particular product, this button will be enable.*

    - If product is out of stock, the button "Add to bag" is disabled;

    ![Product's details page. Product out of stock](documentation/features/product_details/product_out_of_stock.png)

  - Product's price:
  
    ![Product's details page. Values variations](documentation/features/product_details/values_for_spider.png)

    The price of the product can be different depending on the product's values. In the above example, the price for the tarantula starts from $40  and increases to $120.
    
      - If the user chooses the particular value of the product, the price of the product will be specified:

      ![Product's details page. Change price on checked values 1](documentation/features/product_details/show_price_on_value.png)

      ![Product's details page. Change price on checked value 2](documentation/features/product_details/show_price_on_value_change.png)

    - If there is a discount, the price of the product will be displayed with the discount.
    
      ![Product's details page. Price with discount](documentation/features/product_details/product_detail_discount.png)
      
  - Product's quantity:

    ![Product's details page. Quantity](documentation/features/product_details/quantity_section.png)

      - If the quantity is limited, the user will see a warning message.

      ![Product's details page. Quantity warning message](documentation/features/product_details/quantity_warning_msg.png)

      - If the user adds the exact quantity of the product that is available right now (7 items in this example), the plus button will be disabled.

      ![Product's details page. Disable plus button](documentation/features/product_details/limited_quantity_plus_disable.png)

      - If the user reduces the quantity of the product, the plus button will be enabled.

      ![Product's details page. Enable plus button](documentation/features/product_details/limited_quantity_plus_enable_after_clicking_minus.png)

  - Add to bag button:

    The functionality of this button has been described above in the values options. It has 2 stages:

    - disabled: the button is disabled when the user has not chosen the values of the product or the product is out of stock;

    ![Product's details page. Add to bag is disable](documentation/features/product_details/add_to_bag_button_disable.png)

    - enabled: the button is enabled when the user has chosen the values of the product and the product is not out of stock and there are not options for a particular product;

    ![Product's details page. Add to bag is enable](documentation/features/product_details/add_to_bag_button_enable.png)

    - If button is enabled, the user can add the product to the bag and the message will appear in the top right corner of the page confirming the success of the operation:
    
      ![Product's details page. Add to bag message](documentation/features/product_details/add_to_bag_msg.png)

  - Request product section:

    - When the user opens the product's details page, the request product section is not displayed till the user starts choosing combinations of the product's options
    
      ![Product's details page. No request message](documentation/features/product_details/request_msg_not_displayed.png)

    - When the user chooses some product's options and there are some units of the products are not present in the store at this moment, he/she will see are message. This message will give the user a chance to request the particular product's options from the store and get notification email when the product is available.
    
      ![Product's details page. Request Product message](documentation/features/product_details/request_msg_displayed.png)

    - If product is out of stock, the request product section is displayed right away.
    
      ![Product's details page. Request message displayed on load](documentation/features/product_details/request_msg_displayed_right_away.png)

  - Modal for requesting a product:

    ![Product's details page. Modal](documentation/features/product_details/modal_product_request.png)

    - There are 2 buttons: "Cancel" and "Send" request. "Cancel" button will cancel the request and closes the modal. "Send" button allows user to request a stock notification email when the product is available.

    - If there are options for a particular product and the user hasn't specified with options combinations he/she wants and user clicks "Send" button, there will a visible highlighted title to remind user to select options and the request will not be sent
    
      ![Product's details page. Options not chosen for the request](documentation/features/product_details/modal_product_request_options_not_chosen.png)

    - If the user has specified with options combinations he/she wants and user clicks "Send" button, the request will be sent, modal window will be closed and the user will see a message confirming the success of the operation.
    
      ![Product's details page. Request sent success](documentation/features/product_details/modal_request_sent_msg.png)

    - If the user has specified with options combinations he/she wants and user clicks "Cancel" button, the request will not be sent and modal window will be closed.

    - If the user has specified with the options combinations he/she wants and user clicks "Send" button, and these options combinations are available in the store at this moment, the request will not be sent, modal window will be closed and the user will see a message:

      ![Product's details page. Enough in stock message](documentation/features/product_details/modal_enough_in_stock_msg.png)

  - Email notifications on stock request:

    When the user requested a product, the user will receive an email notification when the product is available.

    ![Product's details page. Stock request email](documentation/features/product_details/stock_request_email.png)

    When the requested product is available, the user will receive an email notification.

    ![Product's details page. Stock notification email](documentation/features/product_details/stock_answer_email.png)

  *For the mobile version of the site, the product's details page is displayed in a different way.*

  ![Product's details page. Mobile](documentation/features/product_details/product_details_page_mobile.png)

### Wishlist page:

![Wishlist page](documentation/features/wishlist/wishlist_page.png)

This page has following features:

  - Empty wishlist button:
  
    ![Wishlist page. Empty wishlist button](documentation/features/wishlist/wishlist_empty_wishlist_button.png)
    
    - if user unlikes the product, the product will be removed from the wishlist and the user will see a message confirming the success of the operation.

    ![Wishlist page. Empty wishlist message](documentation/features/wishlist/wishlist_remove_item_msg.png)

    - If the user clicks the button, a container with the confirmation will appear:

    ![Wishlist page. Empty wishlist container](documentation/features/wishlist/wishlist_empty_wishlist_container.png)

    - if the user clicks "No", the container will be closed and the wishlist will not be emptied.

    - If the user click "Yes" button, the wishlist will be emptied and the user will see a message confirming the success of the operation.

    ![Wishlist page. Empty wishlist message](documentation/features/wishlist/wishlist_empty_msg.png)

    - If there are no items in the wishlist, the user will see a message:

    ![Wishlist page. Wishlist empty](documentation/features/wishlist/wishlist_empty.png)

    - If there too many items in the wishlist, the user will see a functional page navigation:

    ![Wishlist page. Pages navigation](documentation/features/wishlist/wishlist_pagination.png)


### Product's Review page:

![Product's review page](documentation/features/product_review/product_review_page.png)

This page has all reviews for the product that has been left by the users who purchased the product.

*Due to the lack of time, the database wasn't fully filled; However, all reviews my be seen on this page with page navigation. If there are more than 20 reviews, the user will see a functional page navigation.*

### Bag page:

![Bag page](documentation/features/bag/bag_page.png)

This page has following features:

  - Title with the arrow down button. If user clicks this button, he/she will be redirected to checkout button immediately.
  
    ![Bag page. Title](documentation/features/bag/bag_title.png)
    
    - If user clicks the button, the bag page will be redirected to the checkout page.
    
  - Alert message. It can have to options:

    - If user has subscribed to the newsletter, the message will be displayed:
    
      ![Bag page. User has subscribed](documentation/features/bag/bag_warning_message_coupon.png)

    - If user hasn't subscribed to the newsletter, the message will be displayed:

      ![Bag page. User hasn't subscribed](documentation/features/bag/bag_warning_message.png)

  - Bag table with all items in the bag:
  
    ![Bag page. Bag Table](documentation/features/bag/bag_table.png)

    - If there are no items in the bag, the user will see a message and there would be no bag table:
    
      ![Bag page. No items in the bag](documentation/features/bag/your_bag_is_empty_now.png)

    - Items of the bag:

    ![Bag page. Bag Item](documentation/features/bag/bag_item.png)

      - It has an image of the product, the name of the product, the quantity, the price for the single item, quantity control, the total price for the item, and the remove button.

      - Quantity control provides the user a possibility to change the quantity of the item in the bag.

      ![Bag page. Quantity control](documentation/features/bag/bag_buttons_quantity_control.png)

      - If user clicks the "+" button, the quantity of the item will be increased by 1 and the user will see the message:

      ![Bag page. Quantity control. Message](documentation/features/bag/bag_product_updated_msg.png)

      - If user clicks the "-" button, the quantity of the item will be decreased by 1 (If user has more than 1 items) and the user will see the message:

      ![Bag page. Quantity control. Message](documentation/features/bag/bag_product_updated_msg.png)

      - If user clicks the "-" button and the quantity of the item is 1, the item will be removed from the bag and the user will see the message:

      ![Bag page. Quantity control. Message](documentation/features/bag/product_remove_from_bag_msg.png)

      **Note!** When user updates the quantity of the item in the bag, the total price for the item and the total spending will be updated as well.

      - There is an remove from the bag button, which helps the user to remove the item from the bag regardless of the quantity.

      ![Bag page. Quantity control. Empty Bag button](documentation/features/bag/bag_button_empty_bag.png)

      - When user clicks the button, all items will be removed from the bag and the user will see the message:

      ![Bag page. Empty Bag button. Message](documentation/features/bag/bag_is_empty_now_msg.png)

  - Bag Summary section:

    ![Bag page. Bag Summary](documentation/features/bag/bag_summary.png)

    It has Total sum of the bag and quantity of the items in the bag.

  - Under this section the user may see coupon section for loyal customers:

    ![Bag page. Coupon section](documentation/features/bag/bag_coupon_section.png)

    - If the user inputs the correct coupon code, the price will be reduced by the coupon value

      ![Bag page. Coupon section. Message](documentation/features/bag/bag_coupon_msg.png)

    - If the user inputs the incorrect coupon code, the user will see the message:
    
      ![Bag page. Coupon section. Message](documentation/features/bag/bag_coupon_invalid_msg.png)

  - Checkout button. When the user clicks the button, the bag page will be redirected to the checkout page.
  
    ![Bag page. Checkout button](documentation/features/bag/bag_checkout_button.png)

### Payment page:

![Payment page](documentation/features/payment/payment_page.png)

This page has following features:

  - Title and prefilled form:
  
    ![Payment page. Title and form](documentation/features/payment/payment_form.png)

    - This form is editable and the user can change the data.

    - If the user hasn't set the full name in the profile, the "Customer Name" will be empty:

    ![Payment page. Customer Name](documentation/features/payment/payemnt_form_no_customer_name.png)
    
    - If user has subscribed to the newsletter, the form will be prefilled with the email address.

    - Alert message if the user hasn't set a primary address with empty form:

    ![Payment page. Alert message](documentation/features/payment/payment_form_no_primary_address.png)

  - Under the from the user will see a payment card field with a "Pay button" This button will show the exact price for the order.
  
    ![Payment page. Payment card](documentation/features/payment/payment_form_stripe.png)
    
    - If the user clicks the button, the payment page will be redirected to the confirmation page.

    *If there are any errors in the form, the user will see the messages*
    *Uses is enable to double click on the button to pay the order.*

### Order Placed page:

![Order Placed page](documentation/features/order_placed/order_placed_page.png)

This page has a success message and a button to go to review a customer's orders.

### Promotions Page:

![Promotions page](documentation/features/personnel/promotions/promotions_page.png)

This page is accessible only to the personnel. And only admin is able to add a promotion, render the promotion page and delete the promotion.

The following image shows the promotion page for managers:

![Promotions page. Add promotion Disable](documentation/features/personnel/promotions/no_add_button_manager.png)

When the personnel member clicks on the promotion in the promotions table, the dropdown menu will be displayed with all items in the promotion and link to these items.

![Promotions page. Dropdown menu](documentation/features/personnel/promotions/promo_items.png)

However, only the admin is able to see edit and delete buttons.

The following image shows the promotion dropdown menu for managers:

![Promotions page. Dropdown menu Disable](documentation/features/personnel/promotions/no_buttons_promo_manager.png)

- If admin clicks add promotion button, he will be redirected to add promotion page;

- If admin clicks on the edit button, he will be redirected to edit promotion page;

- If admin clicks on the delete button, the modal will be displayed with a confirmation message;

![Promotions page. Modal](documentation/features/personnel/promotions/promotions_delete_modal.png)

### Add Promotion Page:

![Add Promotion page](documentation/features/personnel/add_promotion/add_promotion_page.png)

This page is accessible only to the admin. It has a form with fields for the promotion name, description, coupon code, discount, start date, end date, and the items that will be included in the promotion.

When the admin clicks "Cancel" button, the admin will be redirected to the promotions page.

When the admin clicks "Save" button, the admin will be redirected to the promotions page.

### Edit Promotion Page:

![Edit Promotion page](documentation/features/personnel/edit_promotion/edit_promotion_page.png)

This page is accessible only to the admin. It has a form with fields for the promotion name, description, coupon code, discount, start date, end date, and the items that will be included in the promotion.

When the admin clicks "Cancel" button, the admin will be redirected to the promotions page.

When the admin clicks "Save" button, the admin will be redirected to the promotions page.

### Create Email Page:

![Create Email page](documentation/features/personnel/create_email/create_email_page.png)

This page is accessible only by personnel. It has a form with fields for the email name, Content and coupon code.

The coupon code field is optional.


When the personnel clicks "Cancel" button, the personnel will be redirected to the emails page.

When the personnel clicks "Save" button, the personnel will be redirected to the emails page.

### Categories Page:

![Categories page](documentation/features/personnel/categories/categories_page.png)

This page is accessible only to the personnel. It has categories table with all categories.

However, only admin is able to delete categories.

The following image shows the categories table for managers:

![Categories page. Disable](documentation/features/personnel/categories/category_manager.png)

Under the title of the Categories title, the personnel member can see a button to add a category.

If the personnel member clicks on the button, the personnel member will be redirected to the add category page.

- Category card for the admin:

  ![Categories page. Category card](documentation/features/personnel/categories/category_card.png)

  - If the admin or other personnel members click on the edit button, the admin will be redirected to the edit category page;

  - If the admin clicks on the delete button, the admin will be redirected to the delete category page;!

### Add Category Page:

![Add Category page](documentation/features/personnel/categories/add_category.png)

This page is accessible only to the personnel. It has a form with fields for the category name and status.

When the personnel clicks "Cancel" button, the personnel will be redirected to the categories page.

When the personnel clicks "Save" button, the personnel will be redirected to the categories page.

### Edit Category Page:

![Edit Category page](documentation/features/personnel/categories/edit_category.png)

This page is accessible only to the personnel. It has a form with fields for the category name and status.

When the personnel clicks "Cancel" button, the personnel will be redirected to the categories page.

When the personnel clicks "Save" button, the personnel will be redirected to the categories page.

### Delete Category Page:

![Delete Category page](documentation/features/personnel/categories/delete_category.png)

This page is accessible only to the admin. It has a form and the list of the products in the category.

When the admin clicks "Cancel" button, the admin will be redirected to the categories page.

When the admin clicks "Delete" button, the admin will be redirected to the categories page.

### Brands Page:

![Brands page](documentation/features/personnel/brands/brands_page.png)

This page is accessible only to the personnel. It has brands table with all brands.

It has a title, "Add brand" button, which will redirect the personnel member to the add brand page. It also has search field, which allows the admin to search for brands.

The main part of the page is dedicated to the brands table.

if the admin or other personnel members click on the brand in the brands table, the admin will be redirected to the brand's details page.

### Add Brand Page:

![Add Brand page](documentation/features/personnel/brands/add_brand.png)

This page is accessible only to the personnel. It has a form with fields for the brand name, description, and status.

When the personnel clicks "Cancel" button, the personnel will be redirected to the brands page.

When the personnel clicks "Add brand" button, the personnel will be redirected to the brands page.

### Brand Details Page:

![Brand Details page](documentation/features/personnel/brands/brand_detail.png)

This page is accessible only to the personnel.

It has full data on the brand:

*Admin view*

![Brand card](documentation/features/personnel/brands/brand_card.png)

*Manager view*

![Brand card](documentation/features/personnel/brands/brand_details_manager.png)

- Name;
- Status;
- How many products are in the brand;
- All products in the brand;
- Description;
- Edit button;
    - if the personnel member clicks on the edit button, the personnel member will be redirected to the edit brand page;
- Delete button; (Only for admin)
    - if the admin clicks on the delete button, the admin will be redirected to the delete brand page;


### Edit Brand Page:

![Edit Brand page](documentation/features/personnel/brands/edit_brand.png)

This page is accessible only to the personnel. It has a pre-filled form with fields for the brand name, description, and status.

When the personnel clicks "Cancel" button, the personnel will be redirected to the brands page.

When the personnel clicks "Save changes" button, the personnel will be redirected to the brands page.

### Delete Brand Page:

![Delete Brand page](documentation/features/personnel/brands/delete_brand.png)

This page is accessible only to the admin. It has a form and the list of the products in the brand.

When the admin clicks "Cancel" button, the admin will be redirected to the brands page.

When the admin clicks "Delete" button, the admin will be redirected to the brands page.


### Tags Page:

![Tags page](documentation/features/personnel/tags/tags_page.png)

This page is accessible only to the personnel. It has tags table with all tags.

It has a title, "Add tag" button, which will redirect the personnel member to the add tag page. It also has search field, which allows the admin to search for tags.

The main part of the page is dedicated to the tags table.
If the admin or other personnel members click on the tag in the tags table, the admin will be redirected to the tag's details page.


### Tag details Page:

![Tag details page](documentation/features/personnel/tags/tag_detail.png)

This page is accessible only to the personnel.

It has full data on the tag:

  - Name;
  - Status;
  - How many products are in the tag;
  - All products in the tag;
  - Edit button;
      - if the personnel member clicks on the edit button, the personnel member will be redirected to the edit tag page;
  - Delete button;
      - if the personnel member clicks on the delete button, the personnel member will be redirected to the delete tag page;

### Add Tag Page:

![Add Tag page](documentation/features/personnel/tags/add_tag.png)

This page is accessible only to the personnel. It has a form with fields for the tag name and status.

When the personnel clicks "Cancel" button, the personnel will be redirected to the tags page.

When the personnel clicks "Add tag" button, the personnel will be redirected to the tags page.

### Edit Tag Page:

![Edit Tag page](documentation/features/personnel/tags/edit_tag.png)

This page is accessible only to the personnel. It has a pre-filled form with fields for the tag name and status.

When the personnel clicks "Cancel" button, the personnel will be redirected to the tags page.

When the personnel clicks "Save changes" button, the personnel will be redirected to the tags page.

### Delete Tag Page:

![Delete Tag page](documentation/features/personnel/tags/delete_tag.png)

This page is accessible only to the personnel. It has a form with the warning message.

When the personnel clicks "Cancel" button, the personnel will be redirected to the tags page.

When the personnel clicks "Delete" button, the personnel will be redirected to the tags page.



### Product Types Page:

![Product Types page](documentation/features/personnel/product_types/product_types.png)

This page is accessible only to the personnel. It has product types table with all product types.

It has a title, "Add product type" button, which will redirect the personnel member to the add product type page. It also has search field, which allows the admin to search for product types.

The main part of the page is dedicated to the product types table. Product types table has cards with data on each product type:

  - Name;
  - Description;
  - Attributes;
      - If this click on the attribute, the personnel member will see all list of attributes associated with the product type;

      ![Attributes](documentation/features/personnel/product_types/product_types_dropwdown.png)

  - Edit button;
      - if the personnel member clicks on the edit button, the personnel member will be redirected to the edit product type page;

  **The product type card will be viewed as following for managers**

  ![Product type card](documentation/features/personnel/product_types/product_type_manager.png)

  - Delete button; (Only for admin)
      - if the admin clicks on the delete button, the admin will be redirected to the delete product type page;


### Add Product Type Page:

![Add Product Type page](documentation/features/personnel/product_types/add_product_type.png)

This page is accessible only to the personnel. It has a form with fields for the product type name, attributes and description.

When the personnel clicks "Cancel" button, the personnel will be redirected to the product types page.

When the personnel clicks "Add product type" button, the personnel will be redirected to the product types page.

### Edit Product Type Page:

![Edit Product Type page](documentation/features/personnel/product_types/edit_product_type.png)

This page is accessible only to the personnel. It has a pre-filled form with fields for the product type name, attributes and description.

When the personnel clicks "Cancel" button, the personnel will be redirected to the product types page.

When the personnel clicks "Save changes" button, the personnel will be redirected to the product types page.

### Delete Product Type Page:

![Delete Product Type page](documentation/features/personnel/product_types/delete_product_type.png)

This page is accessible only to the personnel. It has no form as the deletion may be dangerous.

It provides a warning message.

And has only "Go back" button.

When the personnel clicks "Go back" button, the personnel will be redirected to the product types page.

### Attributes Page:

![Attributes page](documentation/features/personnel/attributes/attributes.png)

This page is accessible only to the personnel. It has attributes table with all attributes.

It has a title, "Add attribute" button, which will redirect the personnel member to the add attribute page. It also has search field, which allows the admin to search for attributes.

The main part of the page is dedicated to the attributes table. Attributes table has cards with data on each attribute:
  - Name;
  - Description;
  - Values associated with the attribute;
      - If this click on the value, the personnel member will see all list of values associated with the attribute;
      ![Attributes](documentation/features/personnel/attributes/attribut_card_dropdown.png)
  - Edit button;
      - if the personnel member clicks on the edit button, the personnel member will be redirected to the edit attribute page;

  **The attribute card will be viewed as following for managers**

  ![Attribute card](documentation/features/personnel/attributes/attribute_card_manager.png)

  - Delete button; (Only for admin)
      - if the admin clicks on the delete button, the admin will be redirected to the delete attribute page;


### Add Attribute Page:

![Add Attribute page](documentation/features/personnel/attributes/add_attribute.png)

This page is accessible only to the personnel. It has a form with fields for the attribute name, description and values.

When the personnel clicks "Cancel" button, the personnel will be redirected to the attributes page.

When the personnel clicks "Add attribute" button, the personnel will be redirected to the attributes page.

### Edit Attribute Page:

![Edit Attribute page](documentation/features/personnel/attributes/edit_attribute.png)

This page is accessible only to the personnel. It has a pre-filled form with fields for the attribute name, description and values.

When the personnel clicks "Cancel" button, the personnel will be redirected to the attributes page.

When the personnel clicks "Save changes" button, the personnel will be redirected to the attributes page.

### Delete Attribute Page:

![Delete Attribute page](documentation/features/personnel/attributes/delete_attribute.png)

This page is accessible only to the personnel. It has no form as the deletion may be dangerous.

It provides a warning message.

And has only "Go back" button.

When the personnel clicks "Go back" button, the personnel will be redirected to the attributes page.

### Values Page:

![Values page](documentation/features/personnel/values/values.png)

This page is accessible only to the personnel. It has values table with all values.

It has a title, "Add value" button, which will redirect the personnel member to the add value page. It also has search field, which allows the admin to search for values.

The main part of the page is dedicated to the values table. Values table has cards with data on each value:
  - Name;
  - Description;
  - number of units assigned to the value;
  - Edit button;
      - if the personnel member clicks on the edit button, the personnel member will be redirected to the edit value page;
    
    **The value card will be viewed as following for managers**

    ![Value card](documentation/features/personnel/values/value_card_manager.png)

  - Delete button; (Only for admin)
      - if the admin clicks on the delete button, the admin will be redirected to the delete value page;


### Add Value Page:

![Add Value page](documentation/features/personnel/values/add_value.png)

This page is accessible only to the personnel. It has a form with fields for the value name, description and number of units.

When the personnel clicks "Cancel" button, the personnel will be redirected to the values page.

When the personnel clicks "Add value" button, the personnel will be redirected to the values page.

### Edit Value Page:

![Edit Value page](documentation/features/personnel/values/edit_value.png)

This page is accessible only to the personnel. It has a pre-filled form with fields for the value name, description and number of units.

When the personnel clicks "Cancel" button, the personnel will be redirected to the values page.

When the personnel clicks "Save changes" button, the personnel will be redirected to the values page.

### Delete Value Page:

![Delete Value page](documentation/features/personnel/values/delete_value.png)

This page is accessible only to the personnel. It has no form as the deletion may be dangerous.

It provides a warning message.

And has only "Go back" button.

When the personnel clicks "Go back" button, the personnel will be redirected to the values page.


### Products table:

![Products table](documentation/features/personnel/products_table/products_table.png)

THis page is accessible only to the personnel. It has products table with all products.

It has a title, "Add product" button, which will redirect the personnel member to the add product page. 

![Products table](documentation/features/personnel/products_table/products_table_heading.png)

It includes a summary on the products in store as well.

It also has search field, which allows the admin/personnel to search for products.

![Products table](documentation/features/personnel/products_table/products_table_search_bar.png)

The main part of the page is dedicated to the products table. Products table has cards with data on each product:

![Products table](documentation/features/personnel/products_table/products_table_item.png)

  - ID;
  - Name;
  - Category;
  - Number of tags;
  - Brand;
  - Number of images;
  - If the product is on sale;
  - Number of units;
  
  
  If the personnel member clicks on the product, the personnel member will be redirected to the product page.

### Product full data Page:

![Product full data page](documentation/features/personnel/product_full/product_full.png)

This page is accessible only to the personnel. It has a table with all products.

It has a heading section, full data on the product, images, units for the product

- Heading section has a title, label "New" (if product is added recently to the store), Id, status, and 3 buttons:

  ![Product full data page](documentation/features/personnel/product_full/product_full_heading.png)

  - Edit button;
      - if the personnel member clicks on the edit button, the personnel member will be redirected to the edit product page;

  - Delete button;
      - if the personnel member clicks on the delete button, the personnel member will be redirected to the delete product page;

  - View in store button;
      - if the personnel member clicks on the view in store button, the personnel member will be redirected to the product's store page;

- Additional data on the product:
  ![Product full data page](documentation/features/personnel/product_full/product_full_add_data.png)

    It has the following  features:
    
    - description;

    - Category;
        - if the personnel member clicks on the category, the personnel member will be redirected to the category page;

    - Brand;
        - if the personnel member clicks on the brand, the personnel member will be redirected to the brand page;

    - Tags associated with the product and their total number;
        - if the personnel member clicks on the tag, the personnel member will be redirected to the tag page;

- Images section:

![Product full data page](documentation/features/personnel/product_full/product_full_images.png)

It has the following  features:

  - Title with the number of images;

  - Add image button;
      - if the personnel member clicks on the add image button, the personnel member will see a modal window with a form for uploading an image;

      ![Product full data page](documentation/features/personnel/product_full/add_image_modal.png)

      - Modal has the following features:

          - Image id (automatically generated).

          - Choose file button;

          - Alt text field;

          - Checkbox for default image;

          - Checkbox for active image;

          - 2 buttons: "Close" and "Save changes"

      - If the personnel member didn't fill out the form correctly, the personnel member will see a message with the error.

      ![Product full data page](documentation/features/personnel/product_full/add_image_modal_error.png)
    
  - Image cards with the setting displayed for default and active images, edit, delete buttons and the image itself:

      - if the personnel member clicks on the edit button, the personnel member will a modal window with a form for editing the image;

      ![Product full data page](documentation/features/personnel/product_full/edit_image_modal.png)

      - If the personnel member clicks delete button, the personnel member will see a confirmation window with a warning message.

      ![Product full data page](documentation/features/personnel/product_full/delete_image_modal.png)


- Units section:

  ![Product full data page](documentation/features/personnel/product_full/product_full_units.png)

  It has the following  features:

    - Title with the number of units;

    - Add unit button, which will redirect the personnel member to the add unit page;
    
    - Unit cards with the data on the unit:
      - status;

      - SKU;

      - UPC;

      - Values;

      - Weight;

      - Promo;

      - Price options;

      - Stock numbers with colorful background to make sure the stock is in noticed:

      ![Product full data page](documentation/features/personnel/product_full/units_cards_stock.png)

    If the user click on the unit card, the personnel member will be redirected to the unit page;


### Add Product Page:

![Add Product page](documentation/features/personnel/product_full/add_product.png)

This page is accessible only to the personnel. It has a form for adding a product.

It has the following fields:

- Name;
- Description;
- Category;
- Tags;
- Brand;
- Status;
- 2 buttons: "Cancel" and "Save changes";

  - If the personnel member clicks on the "Cancel" button, the personnel member will be redirected to the products page;
  - If the personnel member clicks on the "Save changes" button, the personnel member will be redirected to the products page;


### Edit Product Page:

![Edit Product page](documentation/features/personnel/product_full/edit_product.png)

This page is accessible only to the personnel. It has a form for editing a product.

It has the the same fields as the add product page. The only difference is that the personnel member will see the product's data in the fields.

  - If the personnel member clicks on the "Cancel" button, the personnel member will be redirected to the product full data page and changes will be lost;
  - If the personnel member clicks on the "Save changes" button, the personnel member will be redirected to the product full data page and changes will be saved;


### Delete Product Page:

![Delete Product page](documentation/features/personnel/product_full/delete_product.png)

This page is accessible only to the personnel. It has a form for deleting a product.

It also has a name of the product, the number of units related to this product, and a warning message.

Under the warning message, there is a "Cancel" button and a "Delete" button.

- If the personnel member clicks on the "Cancel" button, the personnel member will be redirected to the product full data page;

- If the personnel member clicks on the "Delete" button, the personnel member will be redirected to the products page;

### Stock Units table:

![Stock Units table](documentation/features/personnel/units/units_table.png)

This page is accessible only to the personnel. It has a table with all stock units.

It has search field, where the personnel member can search for a unit by SKU, UPC, or values.

The stock units table has unit's cards with the data on the unit:

  - status;

  - SKU;

  - UPC;

  - Values;

  - Weight;

  - Promo;

  - Price options;

  - Stock numbers with colorful background to make sure the stock is in noticed:

Page navigation if there more than one page.

### Unit Page:

![Unit page](documentation/features/personnel/units/unit_card.png)

This page has the following features:

- "Back to products" button, which will redirect the personnel member to the products page;
- Name of the product  of the unit and the label if the product is new;
- "Edit" button, which will redirect the personnel member to the edit unit page;
- "Delete" button, which will redirect the personnel member to the delete unit page;
- Data on the unit:
  - status;
  - SKU;
  - UPC;
  - Values;
  - Weight;
  - Promo;
  - Price table;
  - Stock table:
    - Stock numbers with colorful background to make sure the stock is in noticed;
    - Purchased units' amount;
    - Left units' amount;
    - Sold units' amount;
    - Last checked date;
    - Inconsistency; (if there is some inconsistency, the personnel member will see a red background);

    ![Unit page. Stock inconsistency](documentation/features/personnel/units/stock_inconsistency.png)

  *If the personnel member is admin, the admin will see additional buttons:*
    - "Update stock" button, which will redirect the personnel member to the update stock page;
    - "Delete" button, which will redirect the personnel member to the delete unit page;

    If there is not stock for the unit, the personnel member will not see a stock table and there will be a message: "Stock not found" and "Add stock" button, which leads to the add stock page;

    ![Unit page. Stock not found](documentation/features/personnel/units/unit_card_no_stock.png)


  *For the managers this unit detail card will look as follows:*

![Unit page. Manager](documentation/features/personnel/units/unit_stock_manager.png)

![Unit page. Manager. Stock inconsistency](documentation/features/personnel/units/stock_not_found_manager.png)

### Add Unit Page:

![Add Unit page](documentation/features/personnel/units/add_unit.png)

This page is accessible only to the personnel. It has a form for adding a unit.

It has also different fields for different types of products:

![Add Unit page. Selected type. Variant 1](documentation/features/personnel/units/product_type_selected1.png)


![Add Unit page. Selected type. Variant 2](documentation/features/personnel/units/product_type_selected2.png)

The fields with values are appearing on the selected product type and allow personnel member to add all required values.

It has 2 buttons: "Back to product" and "Add Product Unit"

- If the personnel member clicks on the "Back to product" button, the personnel member will be redirected to the units page;

- If the personnel member clicks on the "Add Product Unit" button, the unit will be saved and the form will be cleared in order to let the personnel member to add another unit;

### Edit Unit Page:

![Edit Unit page](documentation/features/personnel/units/edit_unit.png)

This page is accessible only to the personnel. It has a form for editing a unit with pre-filled data.

It has 2 buttons: "Back to product" and "Confirm changes";

  - If the personnel member clicks on the "Back to product" button, the personnel member will be redirected to the units page;
  - If the personnel member clicks on the "Confirm changes" button, the changes will be saved and the personnel member will be able to return to the unit page by clicking on the "Back to product" button;

### Delete Unit Page:

![Delete Unit page](documentation/features/personnel/units/delete_unit.png)

This page is accessible only to the personnel. It has a form for deleting a unit. It has a name of the unit, warning message, and 2 buttons: "Cancel" and "Delete";

- If the personnel member clicks on the "Cancel" button, the personnel member will be redirected to the unit page;

- If the personnel member clicks on the "Delete" button, the personnel member will be redirected to the product page;

### Add Stock Page:

![Add Stock page](documentation/features/personnel/stock/add_stock.png)

This page is accessible only to the admin. It has a form for adding a stock.

The form includes the following fields:

- Checking date;
- Units purchased;
- Units left;
- Units sold;
- 2 buttons: "Cancel" and "Add Stock";

  - If the admin clicks on the "Cancel" button, the admin will be redirected to the unit page;
  - If the admin clicks on the "Add Stock" button, the stock will be saved and the form will be cleared in order to let the admin to add another stock;

The checking date and units purchased fields are necessary for the admin to control any possible inconsistency in the store.

### Update Stock Page:

![Update Stock page](documentation/features/personnel/stock/update_stock.png)

This page is accessible only to the admin. It has a pre-filled form for updating a stock.

The form includes the same fields as the add stock form.

It also has 2 buttons: "Cancel" and "Update Stock";

  - If the admin clicks on the "Cancel" button, the admin will be redirected to the unit page;
  - If the admin clicks on the "Update Stock" button, the stock will be updated and the admin will be redirected to the unit page;

### Delete Stock Page:

![Delete Stock page](documentation/features/personnel/stock/delete_stock.png)

This page is accessible only to the admin. It has a form for deleting a stock. It has a name of the units for which this stock was created, warning message, and 2 buttons: "Cancel" and "Delete";

  - If the admin clicks on the "Cancel" button, the admin will be redirected to the unit page;
  - If the admin clicks on the "Delete" button, the stock will be deleted and the admin will be redirected to the unit page;

### Stock Table Page:

![Stock table page](documentation/features/personnel/stock_table/stock_table.png)

This page is accessible only to personnel. It has the following features:

- Heading with the title, data on how many product's units do not have stock and the "Show" button to see these units;

![Stock table page. Show units without stock button](documentation/features/personnel/stock_table/stock_table_heading.png)

- If "Show" button is clicked, the personnel member may see a table with unit, where each unit has SKU, name of the product, and a link to the unit's product:

![Stock table. Show units without stock table](documentation/features/personnel/stock_table/stock_table_units_without_stock.png)

When personnel member clicks the unit, he/she will be redirected to unit's page to see full data on the unit.

Under this table the used can find a select bar.

![Stock table. Select bar](documentation/features/personnel/stock_table/stock_table_select_bar.png)

When the personnel member/admin clicks particular option, units will be filtered in the table.

![Stock table. Select bar. fewer than 20](documentation/features/personnel/stock_table/stock_table_selected_fewer_than_20.png)]

As it is shown in above example, personnel may find out the number of units, which have < 20 stock units and the full data. In addition, there is also a link to go to the unit details page to find more data on this unit.

The main accent of this page is devoted to stock table itself:

![Stock table. Units](documentation/features/personnel/stock_table/stock_table_units.png)

It has all necessary data on the stock for each unit.

Under the table, the user can find page navigation.

### Orders Page:

![Orders Page](documentation/features/personnel/orders/orders_page.png)

This page is accessible only to personnel. It has all orders data and a search-sort bar.

1. Sort-search bar:

![Orders Page.Sort-search bar](documentation/features/personnel/orders/orders_bar.png)

It allows to search orders by numbers, key and ID. It also empowers personnel to sort orders according to their status.

2. Order's cards.

They include short data on the order and their status. If the personnel member clicks on the order card, he/she will be redirected to order full  details page

### Order full detail Page:

![Order full detail Page](documentation/features/personnel/orders/order_full_detail_admin.png)

This page is accessible only to personnel. It has all data on the order.

However, only the admin can see the rendering order buttons:

*View for the manager*:

![Order full detail Page. View for the manager](documentation/features/personnel/orders/order_full_detail_manager.png)

This page has the following features:

1. "Go to orders" button:

![Order full detail Page. "Go to orders" button](documentation/features/personnel/orders/go_to_orders_button.png)

This button redirects the personnel member to the orders page.

2. "Edit order" and "Delete order" buttons:

![Order full detail Page. "Edit order" and "Delete order" buttons](documentation/features/personnel/orders/edit_delete_order_buttons.png)

Accessible only to the admin.

  - If the admin clicks on the "Edit order" button, the admin will be redirected to the order edit page;

  - If the admin clicks on the "Delete order" button, the order will be deleted and the admin will be redirected to the orders page;

3. Order full details:

![Order full detail Page. Order full details](documentation/features/personnel/orders/order_full_data_admin.png)

*However, only admin or logistics manager are able to see the rendering order status buttons*:

- If the admin or logistics manager clicks on the "Edit" button, the dropdown menu will be opened; the admin can change the order status to "Pending", "Processing", "Completed", "Refunded", "Cancelled" or "In delivery";

Examples:

![Order full detail Page. Order full details. "Edit" button](documentation/features/personnel/orders/order_status_update.png)

![Order full detail Page. Order full details. "Edit" button. "Completed" option](documentation/features/personnel/orders/order_status_completed.png)

![Order full detail Page. Order full details. "Edit" button. "Processing" option](documentation/features/personnel/orders/order_status_processing.png)

![Order full detail Page. Order full details. "Edit" button. "Pending" option](documentation/features/personnel/orders/order_status_refund.png)


4. Order items table:

![Order full detail Page. Order items table](documentation/features/personnel/orders/order_item_admin.png)

Each item has the following data:

- Product name with a link to the product in store;
- Image of the product;
- Product's values;
- Quantity;
- Price;
- Total price;
- 2 buttons accessible only to the admin: "Edit" and "Delete";
    - If the admin clicks on the "Edit" button, the admin will be redirected to the order item edit page;
    - If the admin clicks on the "Delete" button, the order item will be deleted and the admin will be redirected to the order full detail page;

5. Customer's order data including customer's name, phone number, email, address and phone number:

![Order full detail Page. Customer's order data](documentation/features/personnel/orders/order_full_details_customer_data.png)

### Edit Order Item Page:

![Edit Order Item Page](documentation/features/personnel/orders/edit_order_item_page.png)

Accessible only to the admin. This page has the following features:

  - Heading with the title;
  - Form with all necessary data on the order item;
  - "Save" button;
  - "Cancel" button;

### Delete Order Item Page:

![Delete Order Item Page](documentation/features/personnel/orders/delete_order_item.png)

Accessible only to the admin. This page has the following features:

  - Heading with the title;
  - Warning message;
  - "Delete" button;
  - "Cancel" button;

### Edit Order Page:

![Edit Order Page](documentation/features/personnel/orders/edit_order.png)

Accessible only to the admin. This page has the following features:

  - Heading with the title;
  - Form with all necessary data on the order;
  - "Save" button;
  - "Cancel" button;

### Delete Order Page:

![Delete Order Page](documentation/features/personnel/orders/delete_order.png)

  - Heading with the title;
  - Warning message;
  - "Delete" button;
  - "Cancel" button;

### Stock Requests Page:

![Stock Requests Page](documentation/features/personnel/stock_requests/stock_requests.png)

This page is accessible only to personnel. It has all stock requests data and a sort bar.

1. Heading with the title and the number of requests;

![Stock Requests Page. Heading](documentation/features/personnel/stock_requests/stock_requests_heading.png)

2. Sort bar with dropdown menu where all requested products are shown. It allows to sort requests by product.

![Stock Requests Page. Sort bar](documentation/features/personnel/stock_requests/stock_requests_search.png)

3. Stock requests Table:

![Stock Requests Page. Stock requests Table](documentation/features/personnel/stock_requests/stock_requests_table.png)

The table has the following data:

- Product name with a link to the product in store;

- Values of the product requested;

- Quantity;

## Allauth and Access pages:


### Access Page:

![Access Page](documentation/features/allauth_access/access_denied.png)

### 404 and 500 pages:

It handles 2 types of errors:

- 404 error;
- 500 error;

Example of 404 error:

![404 error](documentation/features/allauth_access/404.png)


![500 error](documentation/features/allauth_access/500.png)

### Logout Page:

![Logout Page](documentation/features/allauth_access/logout.png)

### Signup Page:

![Signup Page](documentation/features/allauth_access/sign_up.png)


### Login Page:

![Login Page](documentation/features/allauth_access/login.png)

### Forgot Password Page:

![Forgot Password Page](documentation/features/allauth_access/reset_password_request.png)

### Reset password Page:

![Reset password Page](documentation/features/allauth_access/change_password_form.png)

### Change Password Page Success:

![Change Password Page Success](documentation/features/allauth_access/change_password_successful.png)