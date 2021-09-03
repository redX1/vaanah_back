from os import name
import shippo
from django.conf import settings
import requests
from .models import Address

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
        return requests.get(url=url, params=params, headers=headers)

class ShippoAddressAPI(object):

    def create(self, address: Address):
        return shippo.Address.create(
            name=address.name,
            company=address.company,
            street1=address.street1,
            city=address.city,
            state=address.state,
            zip=address.zip_code,
            country=address.country,
            phone=address.phone,
            email=address.email
        )