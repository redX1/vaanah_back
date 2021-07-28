from stripe.api_resources import payment_intent
from .models import Fund

class FundController(object):
    def create(self, amount, currency, customer, payment, wallet, payment_intent_id, product):
        fund = Fund.objects.create(
            amount=amount,
            currency=currency,
            customer=customer,
            payment=payment,
            wallet=wallet,
            payment_intent_id=payment_intent_id,
            product=product
        )

        return fund

