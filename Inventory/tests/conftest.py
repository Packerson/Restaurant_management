from random import random

import faker
import pytest
from django.test import Client

from Inventory.models import Product, Company

choices = ["QTY", "L", "KG"]


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def product():
    product = Product.objects.create(name='Product1', unit=["QTY"],
                                     amount=(3 + 1 / 100), gross_price=(201 / 100) + 5,
                                     net_price=(101 / 100))
    return product

@pytest.fixture
def companys():
    company = Company.objects.create(name=faker.name(),
                                     nip=random.randint(1000000000, 9999999999),
                                     address=faker.address())
    return company
