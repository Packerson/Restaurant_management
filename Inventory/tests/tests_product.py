import pytest
from django.urls import reverse

from Inventory.models import Product

# Create your tests here.
"""Tests:

    # -dodanie produktu
    # -usunięcie produktu
    # -zmiana produktu
    # -order by
    # -dodanie firmy
    # -usuniecie
    # -zmiana
    # -order by
    # -dodanie faktury
    # -usuniecie faktury
    -zmiana 
    -dodanie produktu do faktury
    -usuniecie produktu
    -zmiana produktu
    -dodanie produktu do inventory
    -usuniecie
    -zmiana
    -stworzenie użytkownika"""


@pytest.mark.django_db
def test_product(product):
    """checking if its working"""
    assert len(Product.objects.all()) == 3
    assert Product.objects.get(name='Product1') == product[0]


@pytest.mark.django_db
def test_product_add(client):
    """add product test"""
    response = client.post(reverse("product_add"),
                           {"name": "abc", "unit": "L",
                            "amount": 1,
                            'gross_price': 2, 'net_price': 1})

    assert response.status_code == 200
    assert len(Product.objects.all()) == 1

    product = Product.objects.first()

    assert product.name == "abc"
    assert product.unit == "L"
    assert product.amount == 1


@pytest.mark.django_db
def test_product_remove(client, product):
    """remove product test"""
    response = client.post(reverse('product_delete', kwargs={'pk': product[1].id}))

    assert response.status_code == 302
    assert len(Product.objects.all()) == 2


@pytest.mark.django_db
def test_product_update(client, product):
    """update product test"""
    response = client.post(reverse('product_edit', kwargs={'pk': product[0].id}),
                           {"name": "abc", "unit": "L",
                            "amount": 1,
                            'gross_price': 2, 'net_price': 1})

    product_updated = Product.objects.first()

    assert product_updated.name == 'abc'


@pytest.mark.django_db
def test_products_list(client, product):
    """Test for checking order_by: (name) """
    response = client.get(reverse('product_list'))

    assert response.status_code == 200
    assert list(response.context["products_list"]) == [product[1], product[0],
                                                       product[2]]
