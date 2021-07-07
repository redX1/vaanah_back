import random
import string

class Util:
    def getRandomString():
        letters = string.ascii_uppercase

        return ''.join(random.choice(letters) for i in range(5))
