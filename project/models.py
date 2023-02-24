from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=30,null=True)
    phoneNumber = models.CharField(max_length=11,null=True)
    avatar = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name

class Book(models.Model):
    
    name = models.CharField(max_length=40,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True) 
    price = models.IntegerField()
    image = models.ImageField(null=True,blank=True)
    description = models.TextField(null=True)
    def __str__(self):
        return self.name
class comment(models.Model):
    customer = models.ForeignKey(customer,on_delete=models.CASCADE,blank=True,null=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE,blank=True,null=True)
    review = models.TextField(null=True)
class Cart(models.Model):
    customer = models.ForeignKey(customer,on_delete=models.CASCADE,blank=True,null=True) 
    Created_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    address = models.CharField(max_length=200,null=False)
    city= models.CharField(max_length=200,null=False)
    
    
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
        
class OrderItem(models.Model):
    product = models.ForeignKey(Book,on_delete=models.CASCADE,blank=True,null=True)
    order = models.ForeignKey(Cart,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_add = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price*self.quantity
        return total
        
    
    
