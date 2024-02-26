from django.db import models
from category.models import Category
# Create your models here.
class Products(models.Model):
    pname = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2,null = True)
    
    description = models.TextField(max_length=500,unique=True)
    image = models.ImageField(upload_to='media')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_listed = models.BooleanField(default = True)
    in_stock = models.IntegerField(null = True)
    imagea = models.ImageField(upload_to='media')
    imageb = models.ImageField(upload_to='media')
    quantity = models.PositiveIntegerField(default=0)

    
    
    def __str__(self):
        return self.pname
    

class Variant(models.Model):
    products = models.ForeignKey(Products,on_delete = models.CASCADE)
    unit_choices = [
        ('500g','500 grams'),
        ('1kg','1 kilogram'),
        ('2kg','2 kilogram'),
    ]
    unit = models.CharField(max_length = 50, choices = unit_choices)
    v_quantity = models.PositiveBigIntegerField(default = 0)
    v_price = models.DecimalField(max_digits = 10, decimal_places=2)


    def __str__(self):
        return f"{self.products.pname} - {self.get_unit_display()}"

class Productoffer(models.Model):
    product_id = models.ForeignKey(Products,on_delete = models.CASCADE,null = True, related_name = "offer")
    variant_id = models.ForeignKey(Variant,on_delete = models.CASCADE,null = True, related_name = "offers")
    percentage = models.IntegerField()
    is_listed = models.BooleanField(default = False)

class Categoryoffer(models.Model):
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE,null = True,related_name = "offers")
    variant_i = models.ForeignKey(Variant,on_delete = models.CASCADE,null = True)
    percentage = models.IntegerField()
    is_listed = models.BooleanField(default = False)    