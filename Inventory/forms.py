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



def choices_invoices():
    """function for select/choices list in Inventory view"""
    invoices = Invoice.objects.all()
    invoices_list = []
    for invoice in invoices:
        invoices_list.append((invoice.id, invoice.number))
    return invoices_list


class AddInvoiceToInventoryForm(forms.Form):
    """Form for adding invoice to inventory"""
    invoice = forms.ChoiceField(choices=choices_invoices)

    def clean_invoice(self):
        invoice = Invoice.objects.get(id=self.cleaned_data['invoice'])
        products_on_invoice = ProductQuantity.objects.filter(invoice=invoice.pk)
        inventory = Inventory.objects.all()
        for products in products_on_invoice:
            if not Inventory.objects.filter(product=products.product.id):
                Inventory.objects.create(product=products.product, amount=products.amount)
            elif Inventory.objects.filter(product=products.product.id):
                product_updated = Inventory.objects.get(product=products.product.id)
                product_updated.amount += products.amount
                product_updated.save()
            else:
                raise forms.ValidationError("Something goes wrong")
        return invoice.id
