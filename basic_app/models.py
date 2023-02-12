from django.db import models

# Create your models here.


class Flat(models.Model):
    flat = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    rent_price_month = models.IntegerField()
    price = models.IntegerField()
    room = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.address}, кв. {self.room}'

"""
class Employee(models.Model):
    employee = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.employee_name}'
"""


class Client(models.Model):
    client = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    discount_card = models.CharField(max_length=30, null=True, unique=True)
    phone_number = models.CharField(max_length=12, null=True, unique=True)
    desc = models.CharField(max_length=1023, null=True)
    bonuses = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    order = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_ts = models.DateTimeField(auto_now_add=True)
    date_from = models.DateField()
    date_to = models.DateField()
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    price = models.IntegerField()
    bonuses_used = models.IntegerField()
    bonuses_accrued = models.IntegerField()

    def __str__(self):
        return f'{self.order}'







