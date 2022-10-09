from django.db import models
# nie robiłem migracji jeszcze
CAPACITY_CHOICES = (
    (1, "piece"),
    (2, "liter"),
    (3, 'kilogram')
)


class Invoice(models.Model):
    pass


class ListOfGoods(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(choices=CAPACITY_CHOICES)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2)
    net_price = models.DecimalField(max_digits=10, decimal_places=2)
    invoice = models.ManyToManyField(Invoice)
    data = models.DateField(auto_now_add=True)


class Company(models.Model):
    pass


class Inventory(models.Model):
    pass


class Ingredients(models.Model):
    pass
