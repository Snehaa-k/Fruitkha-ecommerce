from django.db import models
from products.models import Variant,Products
from home.models import Usermodelss,Useraddress
# Create your models 

class CartItem(models.Model):
    user_id = models.ForeignKey(Usermodelss,on_delete = models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    Variant_id = models.ForeignKey(Variant,on_delete = models.CASCADE)
    c_quantity = models.PositiveBigIntegerField(default = 0)
    total = models.IntegerField(blank=True,null=True)
    
    
    def __str__(self) -> str:
        return f"{self.product_id.name}"
    
    

class order_details(models.Model):
    userid = models.ForeignKey(Usermodelss,on_delete=models.CASCADE)
    product_name=models.ForeignKey(Products,on_delete=models.CASCADE) 
    variant_unit=models.ForeignKey(Variant,on_delete=models.CASCADE)
    address = models.ForeignKey(Useraddress,on_delete=models.CASCADE)
    pay_method = models.CharField(max_length=50)
    total_amount = models.BigIntegerField(default=0)
    is_cancel = models.BooleanField(default=False)
     