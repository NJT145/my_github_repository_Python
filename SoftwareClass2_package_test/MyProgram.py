from my_package import *

a = Car()   # Car inside __all__ list
print x     # x inside __all__ list
# cannot import Wheel since it is
# not in __all__ list inside __init__.py module
# b = Wheel()