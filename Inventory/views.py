from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from Inventory.forms import ProductForm, AddUserForm, \
    PasswordChange, CompanyForm, InvoiceForm, InvoiceDetailsForm, \
    InventoryForm, AddInvoiceToInventoryForm
from Inventory.models import Product, Company, Invoice, ProductQuantity, \
    Inventory

"""Pamiętać!"""


"""Add tests for invoice_inventory_add """
""" https://www.codementor.io/@lakshminp/handling-multiple-forms-on-the-same-page-in-django-fv89t2s3j """
"""w przyszłości wyszukiwarka produktów i firm z bazy danych"""

"""pomyśleć nad dodaniem zapytania ,czy na pewno usunął ? w JavaScripcie?"""

"""fasInventory application for restaurants based on my previous professional expierence (7 years as a chef)
Aplication allows for creating user accounts with login access, creating product and supplier database, creating invoices, updating inventory based on invoice contentstAPI, PANDAS"""


def home(request):
    """main page"""
    return render(request, "main.html")


def login_view(request):
    """login view"""
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login!")
            return redirect("main")
        else:
            messages.warning(request, "Mistake in login or password")
            return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("main")


@transaction.atomic
def add_user_view(request):
    """create user"""
    if request.method == "GET":
        return render(request, "add_user.html", {"form": AddUserForm()})
    else:
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Register success!")
            return redirect("login")
        else:
            messages.warning(request, form.errors)
            return render(request, "add_user.html", {"form": AddUserForm()})


@login_required
@transaction.atomic
def change_password_view(request):
    """changing password"""

    if request.method == "GET":
        return render(request, "change_password.html",
                      {"form": PasswordChange(request.user)})
    else:
        form = PasswordChange(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed")
            return redirect("login")
        else:
            messages.warning(request, form.errors)
            return render(request, "change_password.html",
                          {"form": PasswordChange()})


class ProductView(View):
    """Product list view"""

    def get(self, request):
        products = Product.objects.order_by('name')
        if len(products) == 0:
            messages.info(request, "No products in database")

        """create pagination, condition 50 products on page"""
        paginator = Paginator(products, 50)
        page = request.GET.get('page')
        products_list = paginator.get_page(page)
        ctx = {'products_list': products_list}
        return render(request, "product-list.html", ctx)


class ProductAddView(View):
    """add product"""

    def get(self, request):
        form = ProductForm()
        context = {'form': form}
        return render(request, 'product-add.html', context)

    def post(self, request):
        form = ProductForm(request.POST)
        context = {'form': form}
        with transaction.atomic():
            if form.is_valid():
                form.save()
                messages.info(request, "Product added")
                return render(request, 'product-add.html', context)

            messages.info(request, 'something went wrong')
            return render(request, 'product-add.html', context)


class ProductUpdateView(View):
    """Update product, initial value"""

    def get(self, request, pk):
        try:
            if Product.objects.get(pk=pk):
                product = Product.objects.get(pk=pk)
                form = ProductForm(initial=
                                   {'name': product.name, 'unit': product.unit,
                                    'amount': product.amount,
                                    'gross_price': product.gross_price,
                                    'net_price': product.net_price})

                context = {'form': form, 'product': product}
                return render(request, 'product-update.html', context)
        except:
            form = ProductForm()
            messages.info(request, f"No product with this ID:{pk}")
            context = {'form': form}
            return render(request, 'product-update.html', context)

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        form = ProductForm(request.POST, instance=product)
        context = {'form': form, 'product': product}
        if form.is_valid():
            form.save()
            messages.info(request, "Product updated")
            return render(request, 'product-update.html', context)

        messages.info(request, 'something went wrong')
        return render(request, 'product-update.html', context)


class ProductDeleteView(View):
    """delete product"""

    def get(self, request, pk):
        product_to_delete = Product.objects.get(pk=pk)
        ctx = {'product_to_delete': product_to_delete}
        return render(request, 'product_delete.html', ctx)

    def post(self, request, pk):
        product_deleted = Product.objects.get(pk=pk)
        messages.info(request, f"Product {product_deleted.name} deleted")
        product_deleted.delete()
        return redirect('product_list')


class CompanyAddView(View):
    """add company"""

    def get(self, request):
        form = CompanyForm()
        context = {'form': form}
        return render(request, 'company_add.html', context)

    def post(self, request):
        pDict = request.POST.copy()
        form = CompanyForm(pDict)
        context = {'form': form}
        with transaction.atomic():
            if form.is_valid():
                form.save()
                form = CompanyForm()
                messages.info(request, 'company added')
                context = {'form': form}
                return render(request, 'company_add.html', context)

            messages.info(request, 'something went wrong')
            return render(request, 'company_add.html', context)


class CompanyListView(View):
    """company list view, order by name"""

    def get(self, request):
        companys = Company.objects.order_by('name')
        ctx = {'companys': companys}
        if len(companys) == 0:
            messages.info(request, 'No company in database')

        """create pagination, condition 50 elements on page"""
        paginator = Paginator(companys, 50)
        page = request.GET.get('page')
        companys_list = paginator.get_page(page)
        ctx = {'companys_list': companys_list}
        return render(request, "company_list.html", ctx)


class CompanyUpdateView(View):
    """Update inforamtion about company, initial value"""

    def get(self, request, pk):
        try:
            if Company.objects.get(pk=pk):
                company = Company.objects.get(pk=pk)
                form = CompanyForm(initial=
                                   {'name': company.name, 'nip': company.nip,
                                    'address': company.address})
                context = {'form': form, 'company': company}
                return render(request, 'company_update.html', context)
        except:
            form = CompanyForm()
            messages.info(request, f"No company with this ID:{pk}")
            context = {'form': form, }
            return render(request, 'company_update.html', context)

    def post(self, request, pk):
        company = Company.objects.get(pk=pk)
        form = CompanyForm(request.POST, instance=company)
        context = {'form': form, 'company': company}
        if form.is_valid():
            form.save()
            messages.info(request, 'Company update')
            return render(request, 'company_update.html', context)

        messages.info(request, 'something goes wrong')
        return render(request, 'company_update.html', context)


class CompanyDelete(View):
    """"delete company"""

    def get(self, request, pk):
        company_to_delete = Company.objects.get(pk=pk)
        ctx = {'company_to_delete': company_to_delete}
        return render(request, 'company_delete.html', ctx)

    def post(self, request, pk):
        """redirect after success deleted"""
        with transaction.atomic():
            company_deleted = Company.objects.get(pk=pk)
            messages.info(request, f"Company {company_deleted.name} deleted")
            company_deleted.delete()
            return redirect('company_list')


class InvoiceAdd(View):
    """add invoice to database"""

    def get(self, request):
        form = InvoiceForm()
        context = {'form': form}
        return render(request, 'invoice_add.html', context)

    def post(self, request):
        """pDict allow to upodate form """
        pDict = request.POST.copy()
        form = InvoiceForm(pDict)
        context = {'form': form}
        with transaction.atomic():

            if form.is_valid():
                form.save()
                form = InvoiceForm()
                messages.info(request, 'Invoice added')
                context = {'form': form}
                return render(request, 'invoice_add.html', context)

        messages.info(request, 'something went wrong')
        return render(request, 'invoice_add.html', context)


class InvoiceUpdateView(View):
    """update information about invoice"""

    def get(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        form = InvoiceForm(initial={'number': invoice.number,
                                    'company': invoice.company,
                                    'date': invoice.date})
        context = {'form': form, 'invoice': invoice}
        return render(request, 'invoice_add.html', context)

    def post(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        form = InvoiceForm(request.POST, instance=invoice)
        context = {'form': form, 'invoice': invoice}

        if form.is_valid():
            invoice.save()
            messages.info(request, 'Invoice updated')
            return render(request, 'invoice_add.html', context)

        messages.info(request, 'something went wrong')
        return render(request, 'invoice_add.html', context)


class InvoiceListView(View):
    """Invoice list"""

    def get(self, request):
        """Order invoices by creating date"""
        invoices = Invoice.objects.order_by('-date')
        if len(invoices) == 0:
            messages.info(request, 'No invoices in base')

        """create pagination and conditions 50 elements on page"""
        paginator = Paginator(invoices, 50)
        page = request.GET.get('page')
        invoices_list = paginator.get_page(page)
        ctx = {'invoices_list': invoices_list}
        return render(request, "invoice_list.html", ctx)


class InvoiceAddProduct(View):
    """Add product to invoice"""

    @staticmethod
    def result_total(pk):
        """Static method for calculate total gross and net value"""
        result_total = []
        invoice = Invoice.objects.get(pk=pk)
        products_list = ProductQuantity.objects.filter(invoice=pk)
        for result in products_list:
            gross = round(result.amount * result.product.gross_price, 2)
            net = round(result.amount * result.product.net_price, 2)
            result_total.append((gross, net))
            """zip for making lists list"""
        total = zip(products_list, result_total)
        context = {'invoice': invoice,
                   'total': total}
        return context

    def get(self, request, pk):
        """initial, passing invoice.id to hidden input """
        invoice = Invoice.objects.get(pk=pk)
        form = InvoiceDetailsForm(initial={'invoice': invoice.id})
        """loop for showing gross and net value in templates"""
        context = self.result_total(pk)
        context['form'] = form
        return render(request, 'Invoice_update.html', context)

    def post(self, request, pk):
        """creating or updating product on invoice"""
        invoice = Invoice.objects.get(pk=pk)
        product = request.POST['product']

        if not ProductQuantity.objects.filter(invoice=invoice, product=product):
            form = InvoiceDetailsForm(request.POST)
            messages.info(request, f"Product added")
            context2 = {'form': form}
        else:
            product_on_invoice = ProductQuantity.objects.get(invoice=invoice,
                                                             product=product)
            form = InvoiceDetailsForm(request.POST, instance=product_on_invoice)
            messages.info(request, "Product updated!")
            context2 = {'form': form}
        context = self.result_total(pk)

        if form.is_valid():
            form.save()
            context = self.result_total(pk)
            context.update(context2)
            return render(request, 'Invoice_update.html', context)

        messages.info(request, "something went wrong")
        context2 = {'form': InvoiceDetailsForm()}
        context.update(context2)
        return render(request, 'Invoice_update.html', context)


class InvoiceDeleteProduct(View):
    """Delete product form invoice"""

    def get(self, request, pk):
        product_to_delete = ProductQuantity.objects.get(pk=pk)
        context = {'product_to_delete': product_to_delete}
        return render(request, 'invoice_delete_product.html', context)

    def post(self, request, pk):
        """After delete redirect to invoice view"""
        with transaction.atomic():
            product = ProductQuantity.objects.get(pk=pk)
            invoice = product.invoice
            messages.info(request, f"Product {product.product.name} deleted form {invoice.number}")
            product.delete()
            return redirect('invoice_edit', pk=invoice.id)


class InvoiceDelete(View):
    """delete Invoice"""

    def get(self, request, pk):
        invoice_to_delete = Invoice.objects.get(pk=pk)
        context = {'invoice_to_delete': invoice_to_delete}
        return render(request, 'invoice_delete.html', context)

    def post(self, request, pk):
        with transaction.atomic():
            invoice_deleted = Invoice.objects.get(pk=pk)
            messages.info(request, f"Invoice {invoice_deleted.number} deleted ")
            invoice_deleted.delete()
            return redirect('invoice_list')


class InventoryView(View):
    """Inventory list"""

    def get(self, request, ):
        form = InventoryForm()
        form_invoice = AddInvoiceToInventoryForm()
        inventory = Inventory.objects.all()
        invoices = Invoice.objects.order_by("-date")
        context = {'form': form, 'inventory': inventory, 'invoices': invoices,
                   'form_invoice': form_invoice}
        return render(request, 'inventory.html', context)

    def post(self, request):
        """Product add or update in inventory"""
        """add product"""
        if 'Add product' in request.POST:

            product_to_add = request.POST['product']
            amount = int(request.POST['amount'])

            if amount > 0:
                if not Inventory.objects.filter(product=product_to_add):
                    """checking if product not exist """

                    form = InventoryForm(request.POST)
                    messages.info(request, "Product added")

                else:
                    inventory_product = Inventory.objects.get(product=product_to_add)
                    form = InventoryForm(request.POST, instance=inventory_product)
                    messages.info(request, "Product updated")

                form_invoice = AddInvoiceToInventoryForm()
                if form.is_valid():
                    form.save()
                    inventory = Inventory.objects.all()
                    context = {'form': InventoryForm(), 'inventory': inventory,
                               'form_invoice': form_invoice}
                    return render(request, 'inventory.html', context)

            else:
                form_invoice = AddInvoiceToInventoryForm()
                messages.error(request, "something went wrong or amount is negative")
                inventory = Inventory.objects.all()
                context = {'form': InventoryForm(), 'inventory': inventory,
                           'form_invoice': form_invoice}
                return render(request, 'inventory.html', context)

        if 'Add invoice' in request.POST:
            """Add invoice to inventory"""
            form = InventoryForm()
            form_invoice = AddInvoiceToInventoryForm(request.POST)
            if form_invoice.is_valid():
                invoice_to_inventory = Invoice.objects.get \
                    (id=form_invoice.cleaned_data['invoice'])
                inventory = Inventory.objects.all()
                messages.info(request, f'Invoice {invoice_to_inventory} '
                                       f'added to inventory')
                context = {'form': form, 'form_invoice': form_invoice,
                           'inventory': inventory}
                return render(request, 'inventory.html', context)


class InventoryDeleteProduct(View):
    """Delete product form Inventory"""

    def get(self, request, pk):
        product_to_delete = Inventory.objects.get(pk=pk)
        context = {'product_to_delete': product_to_delete}
        return render(request, 'inventory_delete_product.html', context)

    def post(self, request, pk):
        """After delete redirect to inventory view"""
        with transaction.atomic():
            inventory = Inventory.objects.get(pk=pk)
            messages.info(request, f'Product {inventory.product.name} '
                                   f'deleted from inventory')
            inventory.delete()
            return redirect('inventory_list')
