from django.db import models

# Create your models here.


class Category(models.Model):
    category_id =models.BigAutoField(primary_key=True,auto_created=True)
    category_name = models.CharField(max_length=255)
 



class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True,auto_created=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product_images/')
    product_code = models.CharField(max_length=255)
    product_stock_quantity = models.IntegerField(default=0)
    product_created_at = models.DateTimeField(auto_now_add=True)
    product_updated_at = models.DateTimeField(auto_now_add=True)
    product_brand = models.CharField(max_length=255, blank=True, null=True)
    product_manufacturer = models.CharField(max_length=255, blank=True, null=True)
    product_is_available = models.BooleanField(default=True)
    # product_is_featured = models.BooleanField(default=False)
