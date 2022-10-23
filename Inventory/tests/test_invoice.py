from datetime import date

import pytest
from django.urls import reverse

from Inventory.models import Company, Invoice


@pytest.mark.django_db
def test_invoice_add(client):
    """add invoice test"""
    # response_company = client.post(reverse("company_add"),
    #                                {"name": "abc", "nip": '1234567891',
    #                                 "address": "random address"})
    company = Company.objects.create(name="abc", nip='1234567891',
                                     address="random address")

    response = client.post(reverse("invoice_add"),
                           {"number": "123", "company": company.id,
                            "date": "2019-10-31"})

    assert response.status_code == 200
    assert len(Invoice.objects.all()) == 1

    invoice = Invoice.objects.first()

    assert invoice.number == "123"
    assert invoice.company == company
    assert invoice.date == date(2019, 10, 31)


@pytest.mark.django_db
def test_invoice_remove(client, invoice, company):
    """remove invoice test"""
    response = client.post(reverse('invoice_delete', kwargs={'pk': invoice[1].id}))

    assert response.status_code == 302
    assert len(Invoice.objects.all()) == 2


# @pytest.mark.django_db
# def test_invoice_update(client, invoice, company):
