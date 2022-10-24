import random
from datetime import date

import pytest
from django.test import Client
from faker import Faker

from Inventory.models import Product, Company, Invoice

choices = ["QTY", "L", "KG"]
faker = Faker('en_US')


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def product():
    product = Product.objects.create(name='Product1', unit=["QTY"],
                                     amount=(3 + 1 / 100), gross_price=(201 / 100) + 5,
                                     net_price=(101 / 100))
    Aproduct2 = Product.objects.create(name='AProduct2', unit=["L"],
                                       amount=(4 + 1 / 100), gross_price=(401 / 100) + 5,
                                       net_price=(201 / 100))
    product3 = Product.objects.create(name='Product3', unit=["KG"],
                                      amount=(6 + 1 / 100), gross_price=(6201 / 100) + 5,
                                      net_price=(106 / 100))
    return product, Aproduct2, product3


@pytest.fixture
def company():
    company1 = Company.objects.create(name='name_test',
                                      nip=random.randint(1000000000, 9999999999),
                                      address='test_address')
    company2 = Company.objects.create(name='Adam Reyes',
                                      nip=random.randint(1000000000, 9999999999),
                                      address=faker.address())
    company3 = Company.objects.create(name='Bryan Barry',
                                      nip=random.randint(1000000000, 9999999999),
                                      address=faker.address())
    return company1, company2, company3


@pytest.fixture
def invoice(company):
    invoice = []
    for i in range(3):
        invoice.append(Invoice.objects.create(number=f"test_number_{i}", company=company[i],
                                              date=date(int(f"200{i}"), 10, 31)))

    return invoice
