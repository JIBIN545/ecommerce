from django.contrib.auth.models import User
from django.db import models
from shop.models import Products
from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    def subtotal(self):
        return self.quantity * self.products.price

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    order_id = models.CharField(max_length=100)
    ordered_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.IntegerField()
    is_ordered = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=100,default='Pending')

class Order_items(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.order.order_id


