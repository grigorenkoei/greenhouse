from django.contrib import admin
from basic_app.models import Flat, FlatType, Client, Order

# Register your models here.
admin.site.register(Flat)
admin.site.register(FlatType)
admin.site.register(Order)
admin.site.register(Client)

