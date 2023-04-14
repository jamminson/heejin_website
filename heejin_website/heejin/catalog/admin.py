from django.contrib import admin

# Register your models here.
from .models import Resin, Product, Client

admin.site.register(Resin)
admin.site.register(Product)
admin.site.register(Client)

