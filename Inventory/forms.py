import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from Inventory.models import Product, Company, Invoice, ProductQuantity, \
    Inventory


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2",
                  "email", "first_name", "last_name")


class PasswordChange(PasswordChangeForm):
    class Meta:
        model = User
        fields = ("old_password", "password1", "password2")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['date']

    def clean_net_price(self, *args, **kwargs):
        net_price = self.cleaned_data['net_price']
        gross_price = self.cleaned_data['gross_price']

        if gross_price <= net_price:
            raise forms.ValidationError("Net price has to "
                                        "be lower than gross price")
        else:
            return net_price


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class DateInput(forms.DateInput):
    input_type = 'date'


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ['products']

        widgets = {
            'date': DateInput()
        }

    def clean_date(self, *args, **kwargs):
        date = self.cleaned_data['date']
        present = datetime.date.today()

        if date > present:
            raise forms.ValidationError("Date is from future")
        else:
            return date


class InvoiceDetailsForm(forms.ModelForm):
    class Meta:
        model = ProductQuantity
        fields = "__all__"

        widgets = {'invoice': forms.HiddenInput()}



class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"
