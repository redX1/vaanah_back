import braintree
from django.conf import settings

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY
    )
)

class BraintreeAPI(object):
    def get_client_token(self):
        return gateway.client_token.generate()

    def transaction_sale(self, data, user=None):
        return gateway.transaction.sale({
            "amount": data['amount'],
            "payment_method_nonce": data['nonce'],
            "device_data": data['device_data'] if 'device_data' in data else None,
            "customer":{
                "email": 'alioune.kanoute@terinnova.com'
                #user.email,
            },
            "options": {
                "submit_for_settlement": True
            }
        })

    def getTransactionObject(self, transaction):
        return {
            'id': transaction.id,
            'graphql_id': transaction.graphql_id,
            'amount': transaction.amount,
            'currency_iso_code': transaction.currency_iso_code,
            'payment_instrument_type': transaction.payment_instrument_type,
            'processor_response_text': transaction.processor_response_text,
            'processor_settlement_response_code': transaction.processor_settlement_response_code,
            'processor_settlement_response_text': transaction.processor_settlement_response_text,
            'settlement_batch_id': transaction.settlement_batch_id,
            'status': transaction.status,
        }