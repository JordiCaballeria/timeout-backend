import stripe
import os

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')

# Crea un cliente de Stripe para hacer un pago
payment = stripe.PaymentIntent.create(amount=500, currency="gbp", payment_method="pm_card_visa")

print(payment)