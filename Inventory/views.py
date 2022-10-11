from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from Inventory.forms import ProductForm, AddUserForm, PasswordChange
from Inventory.models import Product


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
            return redirect("home")
        else:
            messages.warning(request, "Mistake in login or password")
            return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


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
            messages.success(request, "Hasło zmienione")
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
        return render(request, "product-list.html", ctx)


class ProductAddView(View):
    def get(self, request):
        form = ProductForm()
        context = {'form': form}
        return render(request, 'product-add.html', context)

    def post(self, request):
        form = ProductForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            gross_price = form.cleaned_data['gross_price']
            net_price = form.cleaned_data['net_price']
            if gross_price > net_price:
                form.save()
                context['message'] = 'product added'
                return render(request, 'product-add.html', context)
            context['message'] = 'gross price has to be bigger than net'
        return render(request, 'product-add.html', context)


class ProductEdit(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        form = ProductForm(initial=
                           {'name': product.name, 'unit': product.unit,
                            'quantity': product.quantity,
                            'gross_price': product.gross_price,
                            'net_price': product.net_price})
        context = {'form': form, 'product': product}
        return render(request, 'product-add.html', context)

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


class ProductDelete(View):
    def get(self, request, pk):
        with transaction.atomic():
            if Product.objects.filter(pk=pk).exists():
                Product.objects.filter(pk=pk).delete()
                ctx = {'message': "product deleted"}
                return render(request, 'products-list.html', ctx)
            ctx = {'message': "There is no product with this ID"}
            return render(request, 'product-list.html', ctx)
