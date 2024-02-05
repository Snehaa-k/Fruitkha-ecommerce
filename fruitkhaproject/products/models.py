from django.db import models
from category.models import Category
# Create your models here.
class Products(models.Model):
    pname = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    
    description = models.TextField(max_length=500,unique=True)
    image = models.ImageField(upload_to='media')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_listed = models.BooleanField(default = True)
    in_stock = models.IntegerField()
    
    
    def __str__(self):
        return self.pname