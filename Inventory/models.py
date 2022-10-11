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
    capacity = models.IntegerField(choices=CAPACITY_CHOICES)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2)
    net_price = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)


class Invoice(models.Model):
    number = models.TextField(validators=[MaxLengthValidator(25)])
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductAmount')
    data = models.DateField()


class ProductAmount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=4)


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=4)
    data = models.DateField(auto_now_add=True)


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.ManyToManyField(Product)
