from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from Inventory.models import Product, Company, Invoice, ProductQuantity, Inventory


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")


class PasswordChange(PasswordChangeForm):
    class Meta:
        model = User
        fields = ("old_password", "password1", "password2")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['date']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class DateInput(forms.DateInput):
    input_type = 'date'


class InvoiceDetailsForm(forms.ModelForm):
    class Meta:
        model = ProductQuantity
        # fields = '__all__'
        exclude = ['invoice']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ['products']

        widgets = {
            'date': DateInput(),
        }


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"
