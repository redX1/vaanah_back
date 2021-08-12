from .models import CartItem

class CartService(object):

    def itemInCart(self, cart, product_id):
        response = False
        for item in cart.items.all():
            if item.product.id == product_id:
                response = True
                break
        return response

    ''' def addItemsToCart(self, cart, product_items):
        for item in product_items:
            if self.itemInCart(cart, item) == False:
                item = CartItem.objects.get(id=item)
                cart.items.add(item) '''
