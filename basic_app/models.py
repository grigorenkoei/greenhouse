from django.db import models

# Create your models here.


class FlatType(models.Model):
    type = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.type_name}'


class Flat(models.Model):
    flat = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    rent_price_month = models.IntegerField()
    price = models.IntegerField()
    type = models.ForeignKey(FlatType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.address}'


class Employee(models.Model):
    employee = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.employee_name}'


class OrderStatus(models.Model):
    order_status = models.AutoField(primary_key=True)
    order_status_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.order_status_name}'


class Client(models.Model):
    client = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    discount_card = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=12, null=True)
    desc = models.CharField(max_length=1023, null=True)
    bonuses = models.IntegerField()
    tester_flag = models.IntegerField()

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
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order_id}'






