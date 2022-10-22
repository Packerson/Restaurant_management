from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from Inventory.forms import ProductForm, AddUserForm, \
    PasswordChange, CompanyForm, InvoiceForm, InvoiceDetailsForm, \
    InventoryForm
from Inventory.models import Product, Company, Invoice, ProductQuantity, \
    Inventory

"""Pamiętać!"""



"""widok InventoryView (dodać kilka produktów na magazyn, i 
    spróbować później dodać całą fakturę z listy faktur  """

"""update one to one , informacja że produkt już istnieje w bazie?????"""

"""Dodać ograniczenia w dodawaniu faktur tak by nie można było dodać faktury 
        z przyszłości"""

"""Jak dodać messages do redirect"""

def home(request):
    return render(request, "main.html")


def login_view(request):
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
    # zastanowić się nad tym
    # if not request.user.has_perm("auth.change_user") or request.user.id != int(pk):
    #     raise PermissionDenied()

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
    def get(self, request):
        products = Product.objects.order_by('name')
        ctx = {'products': products}
        if len(products) == 0:
            ctx['message'] = 'No products in base'

        """tworzenie paginacji i warunek 50 przepisów na stronę"""
        paginator = Paginator(products, 50)
        page = request.GET.get('page')
        products_list = paginator.get_page(page)
        ctx = {'products_list': products_list}
        return render(request, "product-list.html", ctx)


class ProductAddView(View):
    def get(self, request):
        form = ProductForm()
        context = {'form': form}
        return render(request, 'product-add.html', context)

    def post(self, request):
        form = ProductForm(request.POST)
        context = {'form': form}
        with transaction.atomic():
            if form.is_valid():
                gross_price = form.cleaned_data['gross_price']
                net_price = form.cleaned_data['net_price']
                if gross_price > net_price:
                    form.save()
                    context['message'] = 'product added'
                    return render(request, 'product-add.html', context)
                context['message'] = 'gross price has to be bigger than net'
            return render(request, 'product-add.html', context)


class ProductUpdateView(View):
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
            context = {'form': form, 'message': f"No product with this ID:{pk}"}
            return render(request, 'product-update.html', context)

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        form = ProductForm(request.POST, instance=product)
        context = {'form': form, 'product': product}
        if form.is_valid():
            gross_price = form.cleaned_data['gross_price']
            net_price = form.cleaned_data['net_price']
            if gross_price > net_price:
                product.save()
                context['message'] = 'product update'
                return render(request, 'product-update.html', context)
            context['message'] = 'gross price has to be bigger than net'
            return render(request, 'product-update.html', context)
        context['message'] = 'something went wrong'
        return render(request, 'product-update.html', context)


class ProductDeleteView(View):

    def get(self, request, pk):
        product_to_delete = Product.objects.get(pk=pk)
        ctx = {'product_to_delete': product_to_delete}
        return render(request, 'product_delete.html', ctx)

    def post(self, request, pk):
        Product.objects.filter(pk=pk).delete()
        return redirect('product_list')


class CompanyAddView(View):
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
                context = {'form': form, 'message': 'company added'}
                return render(request, 'company_add.html', context)
            context['message'] = 'something went wrong'
            return render(request, 'company_add.html', context)


class CompanyListView(View):
    def get(self, request):
        companys = Company.objects.order_by('name')
        ctx = {'companys': companys}
        if len(companys) == 0:
            ctx['message'] = 'No companys in base'

        """tworzenie paginacji i warunek 50 przepisów na stronę"""
        paginator = Paginator(companys, 50)
        page = request.GET.get('page')
        companys_list = paginator.get_page(page)
        ctx = {'companys_list': companys_list}
        return render(request, "company_list.html", ctx)


class CompanyUpdateView(View):
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
            context = {'form': form, 'message': f"No company with this ID:{pk}"}
            return render(request, 'company_update.html', context)

    def post(self, request, pk):
        company = Company.objects.get(pk=pk)
        form = CompanyForm(request.POST, instance=company)
        context = {'form': form, 'company': company}
        if form.is_valid():
            company.save()
            context['message'] = 'Company update'
            return render(request, 'company_update.html', context)

        context['message'] = 'something goes wrong'
        return render(request, 'company_update.html', context)


class CompanyDelete(View):
    def get(self, request, pk):
        company_to_delete = Company.objects.get(pk=pk)
        ctx = {'company_to_delete': company_to_delete}
        return render(request, 'company_delete.html', ctx)

    def post(self, request, pk):
        with transaction.atomic():
            Company.objects.get(pk=pk).delete()
            # ctx = {'message': "Company deleted"}
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
                company_form = form.cleaned_data['company']
                company = Company.objects.get(name=company_form)
                invoice = Invoice.objects.create(number=form.cleaned_data['number'],
                                                 company=company,
                                                 date=form.cleaned_data['date'])
                form = InvoiceForm()
                context = {'form': form, 'message': 'Invoice added'}
                return render(request, 'invoice_add.html', context)
            context['message'] = 'something went wrong'
            return render(request, 'invoice_add.html', context)


class InvoiceUpdateView(View):
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
            context['message'] = 'invoice update'
            return render(request, 'invoice_add.html', context)

        context['message'] = 'something went wrong'
        return render(request, 'invoice_add.html', context)

class InvoiceListView(View):
    """Invoice list"""

    def get(self, request):
        """Order invoices by creating date"""
        invoices = Invoice.objects.order_by('-date')
        ctx = {'invoices': invoices}
        if len(invoices) == 0:
            ctx['message'] = 'No invoices in base'
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
            """zip for making liste list"""
        total = zip(products_list, result_total)
        context = {'invoice': invoice,
                   'total': total}
        return context

    def get(self, request, pk):
        form = InvoiceDetailsForm()
        """loop for showing gross and net value in templates"""
        context = self.result_total(pk)
        context['form'] = form
        return render(request, 'Invoice_update.html', context)

    def post(self, request, pk):
        form = InvoiceDetailsForm(request.POST)
        context = self.result_total(pk)
        if form.is_valid():
            invoice = Invoice.objects.get(pk=pk)
            product = form.cleaned_data['product']
            amount = form.cleaned_data['amount']
            # tak albo robić update produktu
            if not ProductQuantity.objects.filter(product=product).filter \
                        (invoice=invoice):
                ProductQuantity.objects.create(product=product, invoice=invoice,
                                               amount=amount)
                context = self.result_total(pk)
                context2 = {'form': form, 'message': 'Product added'}
                context.update(context2)
                return render(request, 'Invoice_update.html', context)
            else:
                updated_product = ProductQuantity.objects.get(product=product,
                                                              invoice=invoice)
                updated_product.amount = amount
                updated_product.save()
            context = self.result_total(pk)
            context2 = {'form': form, 'message': 'Product updated!'}
            context.update(context2)
            return render(request, 'Invoice_update.html', context)

        context2 = {'message': 'something went wrong', 'form': InvoiceDetailsForm()}
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
            invoice_id = product.invoice.id
            product.delete()
            # context = {'message': "Product deleted"}
            return redirect('invoice_edit', pk=invoice_id)


class InvoiceDelete(View):
    """delete Invoice"""

    def get(self, request, pk):
        invoice_to_delete = Invoice.objects.get(pk=pk)
        context = {'invoice_to_delete': invoice_to_delete}
        return render(request, 'invoice_delete.html', context)

    def post(self, request, pk):
        with transaction.atomic():
            Invoice.objects.filter(pk=pk).delete()
            # ctx = {'message': "Invoice deleted"}
            return redirect('invoice_list')


class InventoryView(View):
    def get(self, request, ):
        form = InventoryForm()
        inventory = Inventory.objects.all()
        context = {'form': form, 'inventory': inventory}
        return render(request, 'inventory.html', context)

    def post(self, request):
        form = InventoryForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            amount = form.cleaned_data['amount']
            if not Inventory.objects.filter(product=product):
                Inventory.objects.create(product=product, amount=amount)
                inventory = Inventory.objects.all()
                context = {'form': InventoryForm(), 'message': 'Product added',
                           'inventory': inventory}
                return render(request, 'inventory.html', context)
        else:
            updated_product = Inventory.objects.get(product=request.POST['product'])
            updated_product.amount = request.POST['amount']
            updated_product.save()
        inventory = Inventory.objects.all()
        context = {'form': form, 'message': 'Product updated!',
                   'inventory': inventory}
        return render(request, 'inventory.html', context)


class InventoryDeleteProduct(View):
    """Delete product form Inventory"""

    def get(self, request, pk):
        product_to_delete = Inventory.objects.get(pk=pk)
        context = {'product_to_delete': product_to_delete}
        return render(request, 'inventory_delete_product.html', context)

    def post(self, request, pk):
        """After delete redirect to invoice view"""
        with transaction.atomic():
            inventory = Inventory.objects.get(pk=pk)
            inventory.delete()
            return redirect('inventory_list')
