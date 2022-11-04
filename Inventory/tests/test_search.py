import pytest
from django.urls import reverse

from Inventory.models import Product, Company

@pytest.mark.django_db
def test_search_product(client, product):
    """searching products by name"""

    response = client.post(reverse('search'), {'search': 'Pro'})

    assert list(response.context["products_list"]) == [product[0],
                                                       product[1],
                                                       product[2]]

@pytest.mark.django_db
def test_search_company(client, company):
    """searching companys by name"""

    response = client.post(reverse('search'), {'search': 'e'})

    assert list(response.context["companys_list"]) == [company[0],
                                                       company[1]]


@pytest.mark.django_db
def test_search_company_nip(client, company):
    """searching company by NIP"""

    company_tested = company[0]

    response = client.post(reverse('search'), {'search': '1234567899'})

    assert list(response.context["companys_list_by_nip"]) == [company[0]]
