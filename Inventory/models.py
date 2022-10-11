from django.core.validators import RegexValidator, MaxLengthValidator
from django.db import models

CAPACITY_CHOICES = (
    (1, "piece"),
    (2, "liter"),
    (3, 'kilogram')
)


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nip = models.CharField(unique=True, max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    address = models.TextField()


class Product(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=1, choices=CAPACITY_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2)
    net_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'quantity']


class Invoice(models.Model):
    number = models.TextField(validators=[MaxLengthValidator(25)])
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductQuantity')
    date = models.DateField()


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=4)
    date = models.DateField(auto_now_add=True)


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.ManyToManyField(Product)
