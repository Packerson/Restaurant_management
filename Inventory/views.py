from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from Inventory.forms import ProductForm, AddUserForm, \
    PasswordChange, CompanyForm, InvoiceForm, InvoiceDetailsForm
from Inventory.models import Product, Company, Invoice, ProductQuantity

"""Pamiętać!"""
# zmienić invoiceAddProduct, zrobić metode statyczną!
# zrobić metodę statyczną  do netto i brutto w InvoiceProduct
# zmienić wszędzie hiperlinki

"""Dodać alerty w momencie dodania po raz drugi tego samego produktu do faktury"""
"""Dodać ograniczenia w dodawaniu faktur tak by nie można było dodać faktury z przyszłości"""


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
        context = {'form': form}
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
        with transaction.atomic():
            try:
                if Product.objects.filter(pk=pk).exists():
                    Product.objects.filter(pk=pk).delete()
                    ctx = {'message': "product deleted"}
                    return redirect('product_list')
            except:
                ctx = {'message': "There is no product with this ID"}
                return render(request, 'product-list.html', ctx)


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
        context = {'form': form}
        if form.is_valid():
            company.save()
            context['message'] = 'Company update'
            return render(request, 'company_update.html', context)
        context['message'] = 'something goes wrong'
        return render(request, 'company_update.html', context)


class CompanyDelete(View):
    def get(self, request, pk):
        with transaction.atomic():
            if Company.objects.filter(pk=pk).exists():
                Company.objects.filter(pk=pk).delete()
                ctx = {'message': "Company deleted"}
                return redirect('company_list')
            ctx = {'message': "There is no company with this ID"}
            return render(request, 'company_list.html', ctx)


class InvoiceAdd(View):
    def get(self, request):
        form = InvoiceForm()
        context = {'form': form}
        return render(request, 'invoice_add.html', context)

    def post(self, request):
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


class InvoiceListView(View):
    def get(self, request):
        invoices = Invoice.objects.order_by('-date')
        ctx = {'invoices': invoices}
        if len(invoices) == 0:
            ctx['message'] = 'No invoices in base'

        """tworzenie paginacji i warunek 50 przepisów na stronę"""
        paginator = Paginator(invoices, 50)
        page = request.GET.get('page')
        invoices_list = paginator.get_page(page)
        ctx = {'invoices_list': invoices_list}
        return render(request, "invoice_list.html", ctx)





class InvoiceAddProduct(View):
    """Add product to invoice"""
    @staticmethod
    def result_total(self):
        result_total = []
        invoice = Invoice.objects.get(pk=self)
        products_list = ProductQuantity.objects.filter(invoice=self)
        for result in products_list:
            gross = round(result.amount * result.product.gross_price, 2)
            net = round(result.amount * result.product.net_price, 2)
            result_total.append((gross, net))
        total = zip(products_list, result_total)
        context = {'invoice': invoice,
                   'total': total}

    def get(self, request, pk):
        form = InvoiceDetailsForm()

        """loop for showing gross and net value in templates"""
        context = {'form': form}
        return render(request, 'Invoice_update.html', context)

    def post(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        products_list = ProductQuantity.objects.filter(invoice=pk)
        form = InvoiceDetailsForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            amount = form.cleaned_data['amount']
            # tak albo robić update produktu
            if not ProductQuantity.objects.filter(product=product).filter(invoice=invoice):
                product_quantity = ProductQuantity.objects.create(product=product,
                                                                  invoice=invoice,
                                                                  amount=amount
                                                                  )
                invoice.refresh_from_db()
                context = {'form': form, 'message': 'Product added', 'invoice': invoice,
                           'total': total}
                return render(request, 'Invoice_update.html', context)
        context = {'message': 'something went wrong', 'form': InvoiceDetailsForm(),
                   'invoice': invoice, 'total': total}
        return render(request, 'Invoice_update.html', context)


class InvoiceDelete(View):
    pass
