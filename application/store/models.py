from django.db import models
from django.contrib.auth.models import User

# Create your models here.


RATING = (
    (1,'★☆☆☆☆'),
    (2,'★★☆☆☆'),
    (3,'★★★☆☆'),
    (4,'★★★★☆'),
    (5,'★★★★★'),
)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=64, null=True)
    email = models.CharField(max_length=64, null=True)
    
    def __str__(self):
        return self.user.username if self.user else 'Anonymous Customer'
    

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL,null=True, blank=True,related_name='products', default=1)
    description = models.CharField(max_length=250, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=150, null=True)
    
    
    def __str__(self):
        return str(self.id)
    
    @property
    def cartTotal(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.getTotal for item in orderitems])    
        return total
    
    @property
    def cartItems(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])    
        return total
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True, blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)

    @property
    def getTotal(self):
        total = self.product.price * self.quantity
        return total

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200,null=False)
    city = models.CharField(max_length=200,null=False)
    state = models.CharField(max_length=200,null=False)
    zipcode = models.CharField(max_length=200,null=False)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Review(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True, blank=True, related_name="reviews")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING,default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'Review of {self.product.name if self.product else "Unknown Product"}'

    def getRating(self):
        return self.rating





