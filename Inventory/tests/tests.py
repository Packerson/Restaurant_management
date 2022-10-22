from django.test import TestCase
import pytest

from Inventory.models import Product

# Create your tests here.
"""Pomysły:

    -dodanie produktu
    -usunięcie produktu
    -zmiana produktu
    -dodanie firmy
    -usuniecie
    -zmiana
    -dodanie faktury
    -usuniecie
    -zmiana
    -dodanie produktu do faktury
    -usuniecie
    -zmiana
    -dodanie produktu do inventory
    -usuniecie
    -zmiana
    -stworzenie użytkownika"""

@pytest.mark.django_db
def test_product_model(product):
    assert len(Product.objects.all()) == 1
    assert Product.objects.get(name='Product1') == product
