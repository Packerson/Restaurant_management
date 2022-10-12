from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from Inventory.forms import ProductForm, AddUserForm, \
    PasswordChange, CompanyForm, InvoiceForm, InvoiceDetailsForm
from Inventory.models import Product, Company, Invoice, ProductQuantity

"""Pamiętać!"""
"""Product update i Company update, zwraca błąd gdy jest 
    update tych samych wartość, poodobnie przy update produktow w fakturze
    ,"""

"""Ask mentor about changing password for all users for themself"""


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
def change_password_view(request, pk):
    if not request.user.has_perm("auth.change_user") or request.user.id != pk:
        raise PermissionDenied()

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
                                    'quantity': product.quantity,
                                    'gross_price': product.gross_price,
                                    'net_price': product.net_price})
                context = {'form': form, 'product': product}
                return render(request, 'product-update.html', context)
        except:
            form = ProductForm()
            context = {'form': form, 'message': f"No product with this ID:{pk}"}
            return render(request, 'product-update.html', context)

    def post(self, request, pk):
        form = ProductForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            gross_price = form.cleaned_data['gross_price']
            net_price = form.cleaned_data['net_price']
            if gross_price > net_price:
                product = Product.objects.get(pk=pk)
                product.name = form.cleaned_data['name']
                product.unit = int(form.cleaned_data['unit'])
                product.quantity = form.cleaned_data['quantity']
                product.gross_price = form.cleaned_data['gross_price']
                product.net_price = form.cleaned_data['net_price']
                product.save()
                context['message'] = 'product update'
                return render(request, 'product-update.html', context)
            context['message'] = 'gross price has to be bigger than net'
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
        form = CompanyForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            company = Company.objects.get(pk=pk)
            company.name = form.cleaned_data['name']
            company.nip = int(form.cleaned_data['nip'])
            company.address = form.cleaned_data['address']
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


class InvoiceView(View):
    pass


class InvoiceUpdate(View):
    def get(self, request, pk):
        form = InvoiceDetailsForm()
        invoice = Invoice.objects.get(pk=pk)
        context = {'form': form, 'invoice': invoice}
        return render(request, 'Invoice_update.html', context)

    def post(self, request, pk):
        form = InvoiceDetailsForm(request.POST)
        invoice = Invoice.objects.get(pk=pk)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            product_quantity = ProductQuantity.objects.create(product=product,
                                                              invoice=invoice,
                                                              quantity=quantity
                                                              )
            context = {'form': form, 'message': 'Product added', 'invoice': invoice}
            return render(request, 'Invoice_update.html', context)
        context = {'message': 'something went wrong', 'form': InvoiceDetailsForm(),
                   'invoice': invoice}
        return render(request, 'Invoice_update.html', context)


class InvoiceDelete(View):
    pass
