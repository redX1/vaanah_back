import random
import string
from .models import Order

class Util:
    def getOrderNumber():
        letters = string.ascii_uppercase
        digits = string.digits
        strn = 'OR' + str(len(Order.objects.all()) + 1)
        rand_nb = ''.join(random.choice(digits) for i in range(2))
        rand_str = ''.join(random.choice(letters) for i in range(3))

        return strn + rand_nb +rand_str