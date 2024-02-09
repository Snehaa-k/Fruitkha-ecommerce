from django.db import models
from products.models import Variant,Products
from home.models import Usermodelss
# Create your models 

class CartItem(models.Model):
    user_id = models.ForeignKey(Usermodelss,on_delete = models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    Variant_id = models.ForeignKey(Variant,on_delete = models.CASCADE)
    c_quantity = models.PositiveBigIntegerField(default = 0)
    total = models.IntegerField(blank=True,null=True)
    ptoduct_name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return f"{self.product_id.name}"
    
    def subtotal(self):
        return self.product_id.price * self.quantity