from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.TextField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):

    Category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    Image = models.ImageField(upload_to='photos')
    Name = models.TextField(max_length=255)
    Price = models.IntegerField()
    Quantity = models.IntegerField(default=1, null=True)
    Desc = models.TextField(default="", null=True,  max_length=255)

from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=False, blank=False, default=1)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ContactDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=255)
    second_name = models.TextField(max_length=255)
    address = models.TextField(max_length=255)
    mobile_number = models.BigIntegerField()
    email = models.EmailField(max_length=255, default="")
    skype = models.TextField(max_length=255, null=True, blank=True)

class Checkout_product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Coupon(models.Model):
    code = models.TextField(max_length=255)
    discount = models.IntegerField()
    active = models.BooleanField()

class Billing_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname= models.TextField(max_length=255)
    lname= models.TextField(max_length=255)
    address= models.TextField(max_length=255)
    city= models.TextField(max_length=255)
    zip= models.IntegerField()
    email= models.EmailField(max_length=255)
    phone= models.BigIntegerField()
    fullamount=models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

# model for storing otp
    
class OTP(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp


