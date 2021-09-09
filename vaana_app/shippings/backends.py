from os import name
import shippo
from django.conf import settings
import requests
from .models import Address, Shipment

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

class ShippoShipmentAPI(object):
    def getParcelObjectForApi(self, parcel):
        return {
            "length": parcel['parcel_length'],
            "width": parcel['parcel_width'],
            "weight": parcel['parcel_weight'],
            "height": parcel['parcel_height'],
            "distance_unit": parcel['distance_unit'],
            "mass_unit": parcel['mass_unit']
        }
    def getAddressObjectForApi(self, address):
        return {
            "company": address['company'] if 'company' in address else '',
            "name": address['name'],
            "street1": address['street1'],
            "city": address['city'],
            "state": address['state'],
            "zip": address['zip_code'],
            "country": address['country'],
            "phone": address['phone'],
            "email": address['email'],
        }

    def create(self, shipment):
        parcels = []
        for i in shipment['parcels']:
            parcels.append(self.getParcelObjectForApi(i))
        return shippo.Shipment.create(
            address_from=self.getAddressObjectForApi(shipment['address_from']),
            address_to=self.getAddressObjectForApi(shipment['address_to']),
            parcels=parcels
        )