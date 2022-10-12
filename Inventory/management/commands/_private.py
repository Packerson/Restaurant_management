import random

from faker import Faker

from Inventory.models import Product, Company, Invoice

faker = Faker('en_US')
choices = ["QTY", "L",  "KG"]

def add_products():
    for i in range(1, 150):
        Product.objects.create(name=f'Product{i}', unit=random.choice(choices),
                               quantity=(i + i / 100), gross_price=(i + i / 100) + 5,
                               net_price=(i + i / 100))


def add_companys():
    for i in range(1, 150):
        Company.objects.create(name=faker.name(),
                               nip=random.randint(1000000000, 9999999999),
                               address=faker.address())


