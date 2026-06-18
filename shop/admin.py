from django.contrib import admin

# Register your models here.

from shop.models import Categorys

from shop.models import Products

admin.site.register(Categorys)
admin.site.register(Products)


