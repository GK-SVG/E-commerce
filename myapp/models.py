from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=120,null=True)
    email=models.CharField(max_length=120)

    def __str__(self):
        return str(self.user)

class Product(models.Model):
    name=models.CharField(max_length=150)
    price=models.FloatField()
    digital=models.BooleanField(default=False,null=True,blank=True)
    categary=models.CharField(max_length=50,default='')
    image=models.ImageField(null=True,blank=True,default='')
    def __str__(self):
        return self.name

    @property
    def ImageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url


        

class Order(models.Model):
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(max_length=100,null=True)
    transaction_id=models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping
    
    @property
    def grand_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)
    
    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=150,null=False)
    state=models.CharField(max_length=150,null=False)
    zipcode=models.CharField(max_length=150,null=False)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    