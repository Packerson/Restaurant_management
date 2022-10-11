import random

from Inventory.models import Product


def add_products():
    for i in range(1, 150):
        Product.objects.create(name=f'Product{i}', unit=random.randint(1, 3),
                               quantity=(i+i/100), gross_price=(i+i/100)+5,
                               net_price=(i+i/100))
