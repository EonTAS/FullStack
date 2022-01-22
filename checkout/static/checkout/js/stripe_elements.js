var stripePublicKey = $('#id_stripe_public_key').text().slice(1,-1)
var clientSecret = $('#id_client_secret').text().slice(1,-1)

var stripe = Stripe(stripePublicKey)

var elements = stripe.elements();
var card = elements.create('card')

console.log("hi ")

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

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        var errorDiv = document.getElementById('card-errors');
        console.log("hasdfi")
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
        } else {
            errorDiv.textContent = ''
            if (result.paymentIntent.status === 'succeeded') {
                form.submit()
            }
        }
    })
})