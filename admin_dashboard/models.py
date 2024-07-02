from django.db import models
from django.db.models.signals import pre_delete,pre_save
from django.dispatch import receiver
import os

# Create your models here.

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100) 
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    material = models.CharField(max_length=30)
    style = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=100) 
    image = models.ImageField(upload_to='images/')
    profession = models.CharField(max_length=30)
    feedback = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
#delete the associated image while an instance is removed
@receiver(pre_delete, sender=Banner)
def delete_banner_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.exists(image_path):
            os.remove(image_path)

@receiver(pre_delete, sender=Category)
def delete_category_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.exists(image_path):
            os.remove(image_path)

@receiver(pre_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.exists(image_path):
            os.remove(image_path)


#delete the old image while the image field of an instance is edited
            
@receiver(pre_save, sender=Banner)
def delete_old_banner_image(sender, instance, **kwargs):
    if instance.pk: 
        old_banner = Banner.objects.get(pk=instance.pk)
        if old_banner.image != instance.image: 
            old_image_path = old_banner.image.path
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

@receiver(pre_save, sender=Category)
def delete_old_category_image(sender, instance, **kwargs):
    if instance.pk:
        old_category = Category.objects.get(pk=instance.pk)
        if old_category.image != instance.image:
            old_image_path = old_category.image.path
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

@receiver(pre_save, sender=Product)
def delete_old_product_image(sender, instance, **kwargs):
    if instance.pk:
        old_product = Product.objects.get(pk=instance.pk)
        if old_product.image != instance.image:
            old_image_path = old_product.image.path
            if os.path.exists(old_image_path):
                os.remove(old_image_path)


