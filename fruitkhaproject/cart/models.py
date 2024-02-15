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
    
    

class Orderdetails(models.Model):
    custom_id = models.ForeignKey(Usermodelss,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,null = True) 
    variant_units = models.ForeignKey(Variant,on_delete=models.CASCADE,null = True)
    addr = models.ForeignKey(Useraddress,on_delete=models.CASCADE)
    paymt_method = models.CharField(max_length=50)
    total_amounts = models.BigIntegerField(default=0)
    orders_date = models.DateField()

class Orderditem(models.Model):
    order_id = models.ForeignKey(Orderdetails,on_delete = models.CASCADE)
    user_id = models.ForeignKey(Usermodelss,on_delete = models.CASCADE,null=True)
    address_id = models.ForeignKey(Useraddress,on_delete = models.CASCADE,null = True)
    unit = models.ForeignKey(Variant,on_delete = models.CASCADE,null = True)
    product_n = models.ForeignKey(Products,on_delete = models.CASCADE)
    ex_deliverey = models.DateField()
    status = models.CharField(max_length = 50)
    quantity = models.IntegerField()
    order_number = models.IntegerField()
    total_amount = models.IntegerField()

class Coupon(models.Model):
    cop_name = models.CharField(max_length=50)
    cop_price = models.BigIntegerField()
    code = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField()
    is_listed = models.BooleanField(default=True)

class Proceedtocheck(models.Model):
    user_id = models.ForeignKey(Usermodelss,on_delete = models.CASCADE)
    order_date = models.DateField()
    total_amount = models.BigIntegerField(default=0)
    applyed_coupen = models.ForeignKey(Coupon,on_delete=models.CASCADE,null = True)
    discount_amount = models.BigIntegerField(null = True)
    is_coupenapplyed = models.BooleanField(default=False)


     