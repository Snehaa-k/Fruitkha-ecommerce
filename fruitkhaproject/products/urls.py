from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
     path('',views.productslist,name='productslist'),
     path('addproduct/',views.addproducts,name='addproducts'),
     path('list1/<str:id>',views.is_listed,name='list1'),
     path('edit/',views.editproducts,name='editproducts'),
     path('update/<str:id>',views.updateproduct,name='updateproducts'),
     path('add_variant/<str:id>',views.add_variant,name='addvariant'),
     path('edit_variant_modal/<str:id>',views.edit_variant_modal,name='edit_variant_modal'),

     



    
]