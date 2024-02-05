from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
     path('',views.productslist,name='productslist'),
     path('addproduct/',views.addproducts,name='addproducts'),
     path('list/<str:id>',views.is_listed,name='list'),
     path('edit/',views.editproducts,name='editproducts'),
     path('update/<str:id>',views.updateproduct,name='updateproducts'),
    
]