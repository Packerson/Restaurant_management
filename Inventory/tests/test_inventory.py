import pytest
from django.urls import reverse

from Inventory.models import Inventory, ProductQuantity


@pytest.mark.django_db
def test_inventory(client, product):
    response = client.get(reverse('inventory_list'))

    assert len(Inventory.objects.all()) == 0
    assert response.status_code == 200


@pytest.mark.django_db
def test_inventory_remove_product(client, django_user_model, product):
    """remove product from inventory test"""

    inventory_product = Inventory.objects.create(product=product[0], amount=1)

    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user \
        (username=username, password=password)
    client.force_login(user)

    assert len(Inventory.objects.all()) == 1

    response = client.post(reverse('inventory_delete_product',
                                   kwargs={'pk': inventory_product.id}))

    """redirect"""
    assert response.status_code == 302
    assert len(Inventory.objects.all()) == 0


@pytest.mark.django_db
def test_inventory_add_products(client, product, invoice, company,
                                django_user_model):
    """adding products to inventory"""

    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user \
        (username=username, password=password)
    client.force_login(user)

    """Add product in dictionary is the button name"""
    form = {'product': product[0].id, 'amount': 3, 'Add product': 'Add product'}

    response_1 = client.post(reverse('inventory_list'),
                             {**form})

    products_in_inventory = Inventory.objects.all()
    print(products_in_inventory)
    assert len(products_in_inventory) == 1
    assert products_in_inventory[0].product == product[0]


@pytest.mark.django_db
def test_inventory_add_products_by_invoice(client, product, invoice, company,
                                           django_user_model):
    """adding products to inventory"""

    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user \
        (username=username, password=password)
    client.force_login(user)

    ProductQuantity.objects.create(product=product[0], invoice=invoice[1],
                                   amount=2)

    """Add invoice in dictionary is the button name"""
    form_invoice = {"invoice": invoice[1].id, 'Add invoice': 'Add invoice'}

    response_1 = client.post(reverse('inventory_list'),
                             {**form_invoice})

    products_in_inventory = Inventory.objects.all()
    print(products_in_inventory)
    assert len(products_in_inventory) == 1
    assert products_in_inventory[0].product == product[0]

    # response_2 = client.post(reverse('inventory_list'),
    #                          {'product': product[1].id,
    #                           'amount': 2.55})
    #
    # response_3 = client.post(reverse('inventory_list'),
    #                          {'product': product[2].id,
    #                           'amount': 3.53})
    #
    # products_in_inventory = Inventory.objects.all()
    #
    # assert len(products_in_inventory) == 3
    # assert products_in_inventory[2].amount == 3.53

    # """Amount test, cant be negative"""
    #
    # response_amount_test = client.post(reverse('inventory_list'),
    #                                    {'product': product[2].id,
    #                                     'amount': -3.53})
    #
    # assert response_amount_test.context['message'] == 'Amount cant be negative!'
    #
    # """update product in inventory"""
    #
    # response_update = client.post(reverse('inventory_list'),
    #                               {'product': product[0].id,
    #                                'amount': 100000})
    #
    # product_in_inventory = Inventory.objects.get(product=product[0].id)
    # """updated product is going on last position in tabel"""
    # assert product_in_inventory.amount == 100000
    #
    # """remove products from inventory"""
    #
    # response_remove = client.post(reverse('inventory_delete_product',
    #                                       kwargs=
    #                                       {'pk': products_in_inventory[1].id}))
    #
    # products_in_inventory = Inventory.objects.all()
    # assert len(products_in_inventory) == 2
    # assert response_remove.status_code == 302
