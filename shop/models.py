from django.db import models

# Create your models here.
class Categorys(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,default='')

    image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,default='')
    image = models.ImageField(upload_to='products')
    price = models.IntegerField()
    stock = models.IntegerField()
    available= models.BooleanField(default=True)
    category = models.ForeignKey(Categorys,on_delete=models.CASCADE,related_name="products")

    created = models.DateTimeField(auto_now_add=True)#only once
    updated = models.DateTimeField(auto_now=True)#everytime we modify the record
    def __str__(self):
        return self.name
