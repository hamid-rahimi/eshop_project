from django.db import models
from django.contrib.auth import get_user_model

from product_module.models import Product


class Slider(models.Model):
    title = models.CharField(max_length=250)
    url_title = models.CharField(max_length=250)
    url = models.URLField(max_length=250)
    text = models.TextField()
    image = models.ImageField(upload_to="sliders",)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    
class AdvertisingBanner(models.Model):
    title = models.CharField(max_length=150)
    url = models.URLField(max_length=150)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="banners/%Y/%m/")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
class MoreVisitedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='visited_product')
    ip = models.CharField(max_length=20)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, blank=True, null=True)


class FavoriteProduct(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="favorite_for_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorite_product")
    
    def __str__(self):
        return f"{self.product.title} {self.user.email}"
    
    def delete_item(self):
        return self.delete()
    