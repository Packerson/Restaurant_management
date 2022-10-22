import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ['products']

        widgets = {
            'date': DateInput()
        }
    # def clean_date(self, *args, **kwargs):
    #     date = self.clean_date('date')
    #     print(date)
    #     present = datetime.date.today()
    #     if date > present:
    #         raise forms.ValidationError("Date is from future")

    # def save(self, *args, **kwargs):
    #     print(self.date)
    #
    #     if self.date > datetime.date.today():
    #         raise ValidationError("The date cannot be in the future!")


class InvoiceDetailsForm(forms.ModelForm):
    class Meta:
        model = ProductQuantity
        # fields = '__all__'
        exclude = ['invoice']


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"
