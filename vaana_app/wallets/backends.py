from django.core.exceptions import ObjectDoesNotExist
from .models import Wallet

class WalletController(object):
    def get(self, seller):
        try:
            wallet = Wallet.objects.get(seller=seller)
        except ObjectDoesNotExist:
            wallet = Wallet.objects.create(seller=seller)

        return wallet
        