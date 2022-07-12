let stripePublicKey = stripe_public_key;
let stripe = Stripe(stripePublicKey);
console.log('connected to stripe');
let elem = document.getElementById('submit');
let paymentForm = document.getElementById('payment-form');
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
  base: {
    color: "#000",
    lineHeight: '2.4',
    fontSize: '16px'
  }
};

var card = elements.create("card", {
  style: style
});
card.mount("#card-element");

card.on('change', function (event) {
  var displayError = document.getElementById('card-errors')
  if (event.error) {
    displayError.textContent = event.error.message;
    $('#card-errors').addClass('alert alert-info');
  } else {
    displayError.textContent = '';
    $('#card-errors').removeClass('alert alert-info');
  }
});

let form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
  ev.preventDefault();

  let customerName = document.getElementById("customer-name").value;
  let customerEmail = document.getElementById("customer-email").value;
  let customerPhone = document.getElementById("customer-phone").value;
  let customerAddress = document.getElementById("customer-address").value;
  let customerAddress2 = document.getElementById("customer-address-2").value;
  let customerCountry = document.getElementById("customer-country").value;
  let customerRegion = document.getElementById("customer-region").value;
  let customerCity = document.getElementById("customer-city").value;
  let postCode = document.getElementById("post-code").value;
  // warning message for the user to prevent refreshing the page,
  // which will cause the payment to fail
  let warning = `
    <div class="col-12">
      <div class="alert alert-danger" role="alert">
        Your payment is being processed.
        Please do not refresh the page or close this window!
      </div>
    </div>
  `;
  $('#card-errors').html(warning);

  let formData = new FormData();
  formData.append('full_name', customerName);
  console.log(customerName);
  formData.append('email', customerEmail);
  formData.append('phone', customerPhone);
  formData.append('address1', customerAddress);
  formData.append('address2', customerAddress2);
  formData.append('country', customerCountry);
  formData.append('county_region_state', customerRegion);
  formData.append('city', customerCity);
  formData.append('zip_code', postCode);
  formData.append('order_key', clientsecret);
  formData.append('csrfmiddlewaretoken', CSRF_TOKEN);
  formData.append('action', 'post');

  console.log(clientsecret);
  // loop through formData and console.log all elements
  for (var pair of formData.entries()) {
    console.log(pair[0] + ', ' + pair[1]);
  }
  //to string
  // let data = JSON.stringify(formData);
  // console.log(data);



  stripe.confirmCardPayment(clientsecret, {
    payment_method: {
      card: card,
      billing_details: {
        address: {
          line1: customerAddress,
          line2: customerAddress2
        },
        name: customerName
      },
    }
  }).then(function (result) {
    if (result.error) {
      console.log('payment error')
      console.log(result.error.message);
      error = `
      <div class="col-12">

        <div class="alert alert-danger" role="alert">
          ${result.error.message}
          Please check your card details and try again!
        </div>
      </div>
      `;
      $('#card-errors').html(error);

    } else {
      if (result.paymentIntent.status === 'succeeded') {
        console.log('payment processed')
        window.location.replace(window.location.origin + "/payment/order_placed/");
        // window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
      }
    }
  });






});