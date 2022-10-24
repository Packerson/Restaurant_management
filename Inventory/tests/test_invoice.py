from datetime import date

import pytest
from django.urls import reverse

from Inventory.models import Company, Invoice, ProductQuantity


@pytest.mark.django_db
def test_invoice_add(client):
    """add invoice test"""

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
def test_invoice_date(client, company):
    """test invoice date, date cant be from future"""

    response = client.post(reverse("invoice_add"),
                           {"number": "123", "company": company[0].id,
                            "date": "2033-10-31"})

    assert response.context['message'] == 'something went wrong'


@pytest.mark.django_db
def test_invoice_remove(client, invoice, company):
    """remove invoice test"""
    response = client.post(reverse('invoice_delete', kwargs={'pk': invoice[1].id}))

    assert response.status_code == 302
    assert len(Invoice.objects.all()) == 2


@pytest.mark.django_db
def test_invoice_update(client, invoice, company):
    """update invoice data test"""
    response = client.post(reverse("invoice_update", kwargs={'pk': invoice[0].id}),
                           {"number": "123", "company": company[1].id,
                            "date": invoice[0].date})

    invoice_testes = Invoice.objects.get(number="123")

    assert invoice_testes.date == invoice[0].date
    assert invoice_testes.company != invoice[0].company


@pytest.mark.django_db
def test_invoice_add_product(client, invoice, company, product):
    """Adding product test"""
    response = client.post(reverse("invoice_edit", kwargs={'pk': invoice[2].id}),
                           {'product': product[0].id, 'invoice': invoice[2].id, 'amount': 2})

    invoice_products_test = ProductQuantity.objects.first()

    assert len(ProductQuantity.objects.all()) == 1

    assert invoice_products_test.product.id == product[0].id
    assert invoice_products_test.amount == 2


@pytest.mark.django_db
def test_invoice_update_and_remove_product(client, invoice, company, product):
    """Updating product test"""
    ProductQuantity.objects.create(product=product[0], invoice=invoice[1],
                                   amount=2)
    invoice_products_test = ProductQuantity.objects.first()

    assert invoice_products_test.amount == 2

    response = client.post(reverse("invoice_edit", kwargs={'pk': invoice[1].id}),
                           {'product': product[0].id, 'invoice': invoice[1].id, 'amount': 3})
    invoice_products_test = ProductQuantity.objects.first()

    assert invoice_products_test.product.id == product[0].id
    assert invoice_products_test.amount == 3

    """Testing remove product form invoice"""

    response_remove = client.post(reverse("invoice_product_delete",
                                          kwargs={'pk': invoice_products_test.id}))

    assert len(ProductQuantity.objects.all()) == 0
    assert response_remove.status_code == 302
