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



});