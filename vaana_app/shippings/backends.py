import shippo
from django.conf import settings
import requests

shippo.config.api_key = settings.SHIPPO_API_KEY

class ShippoCarrierAPI(object):

    def all(self, page=None):
        url = 'https://api.goshippo.com/carrier_accounts/'
        params = {
            'page': 1 if page is None else page
        }
        headers = {
            'Authorization': 'ShippoToken ' + settings.SHIPPO_API_KEY
        }
        return requests.get(url=url, params=params, headers=headers)#shippo.CarrierAccount.all()