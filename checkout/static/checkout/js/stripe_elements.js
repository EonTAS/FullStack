var stripePublicKey = $('#id_stripe_public_key').text().slice(1,-1)
var clientSecret = $('#id_client_secret').text().slice(1,-1)

var item = $('#id_project').text()
var stripe = Stripe(stripePublicKey)

var elements = stripe.elements();
var card = elements.create('card')


card.mount('#card-element')

// handle validation errors

card.addEventListener('change', function(event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error){
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `
        $(errorDiv).html(html)
    }
    else {
        errorDiv.textContent = ''
    }
})

// handle form submit

var form = document.getElementById('payment-form');
form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({"disabled": true})
    $('#submit-button').attr('disabled', true)

    $('#loading-overlay').fadeToggle(100);
    
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'item': item
    }
    var url = '/checkout/cache_checkout/'
    $.post(url, postData).done(function() {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1:$.trim(form.street_address1.value),
                        line2:$.trim(form.street_address2.value),
                        city:$.trim(form.town_or_city.value),
                        country:$.trim(form.country.value),
                        state: $.trim(form.county.value)
                    }
                },
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1:$.trim(form.street_address1.value),
                    line2:$.trim(form.street_address2.value),
                    city:$.trim(form.town_or_city.value),
                    country:$.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value)
                }
            }
        }).then(function(result) {
            var errorDiv = document.getElementById('card-errors');
            if (result.error) {
                var html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>
                `
                $(errorDiv).html(html)
                card.update({'disabled':false})
                $('#submit-button').attr('disabled', false)
    
                $('#loading-overlay').fadeToggle(100);
            } else {
                errorDiv.textContent = ''
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit()
                }
            }
        }).fail(function() {
            location.reload()
        })
    })

})