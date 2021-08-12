from .models import OrderItem
import random
import string

class OrderService(object):

    def get_rand_string(self):
        letters = string.ascii_uppercase
        digits = string.digits
        rand_nb = ''.join(random.choice(digits) for i in range(2))
        rand_str = ''.join(random.choice(letters) for i in range(3))

        return rand_nb + rand_str

    def create_order_item(self, cart_item, order):
        
        number = cart_item.product.store.name.replace(" ", "").upper() + self.get_rand_string()
        amount = cart_item.product.price * cart_item.quantity

        return OrderItem.objects.create(
            number=number,
            seller = cart_item.product.created_by,
            amount=amount,
            cart_item=cart_item,
            order=order,
            currency=order.currency
        )
    def create_order_items(self, order):
        for item in order.cart.items.all():
            self.create_order_item(item, order)
