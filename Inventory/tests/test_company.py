import pytest
from django.urls import reverse

from Inventory.models import Company


@pytest.mark.django_db
def test_company(company):
    """checking if its working"""
    assert len(Company.objects.all()) == 3
    assert Company.objects.get(name='name_test') == company[0]


@pytest.mark.django_db
def test_company_add(client):
    """add company """
    response = client.post(reverse("company_add"),
                           {"name": "abc", "nip": '1234567891',
                            "address": "random address"})

    assert response.status_code == 200
    assert len(Company.objects.all()) == 1

    company = Company.objects.first()

    assert company.name == "abc"
    assert company.nip == '1234567891'
    assert company.address == "random address"


@pytest.mark.django_db
def test_company_remove(client, company):
    """remove company test"""
    response = client.post(reverse('company_delete',
                                   kwargs={'pk': company[1].id}))

    assert response.status_code == 302
    assert len(Company.objects.all()) == 2


@pytest.mark.django_db
def test_company_update(client, company):
    """update company test"""
    response = client.post(reverse("company_edit",
                                   kwargs={'pk': company[0].id}),
                           {"name": "abc", "nip": '1234567891',
                            "address": "random address"})

    company_updated = Company.objects.first()

    assert company_updated.name == 'abc'


@pytest.mark.django_db
def test_company_list(client, company):
    """Test for checking order_by (name) list """
    response = client.get(reverse('company_list'))

    assert response.status_code == 200
    assert list(response.context["companys_list"]) == [company[1],
                                                       company[2],
                                                       company[0]]
