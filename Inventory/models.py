from django.core.validators import RegexValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

CAPACITY_CHOICES = (
    ("QTY", "quantity"),
    ("L", "liter"),
    ("KG", 'kilogram')
)


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nip = models.CharField(unique=True, max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    address = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=10, choices=CAPACITY_CHOICES)
    amount = models.FloatField(validators=[MinValueValidator(0, 0)])
    gross_price = models.FloatField(validators=[MinValueValidator(0, 0)])
    net_price = models.FloatField(validators=[MinValueValidator(0, 0)])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.unit}"

    class Meta:
        unique_together = ['name', 'amount']


class Invoice(models.Model):
    number = models.TextField(validators=[MaxLengthValidator(25)])
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductQuantity')
    date = models.DateField()

    def __str__(self):
        return self.number


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0, 0)])

    class Meta:
        unique_together = ['product', 'invoice']


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0, 0)])
    date = models.DateField(auto_now_add=True)


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.ManyToManyField(Product)
