from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
     path('',views.home,name='home'),
     path('login/',views.userloginp,name='userlog'),
     path('signupa/',views.usersignupa,name='usersign'),
     path('about/',views.about,name='about'),
     path('shop/',views.shop,name='shop'),
     path('otp/<str:id>',views.otpver,name='otpver'),
     path('single/<str:id>',views.singleproduct,name='singleproduct'),
     path('logout/',views.userlogout,name='logout'),
     path('cart/',views.cart,name='cart'),
     path('addcart/<str:id>',views.add_cart,name='add_cart'),

     path('search/',views.searchh,name ='searchh'),
     path('deletecart/<str:id>',views.delete_cart,name ='deletecart'),
     path('userprofile/',views.userprofile,name ='userprofile'),
     path('edituserprofile/',views.edituserprofile ,name ='edituserprofile'),
     path('add_address/',views.add_address ,name ='add_address'),
     path('delete_addres/<str:id>',views.delete_addres ,name ='delete_addres'),
     path('checkout/',views.checkout ,name ='checkout'),
     path('order/',views.orderplace ,name ='orderplace'),
     path('place_order/',views.place_order ,name ='place_order'),
     path('order_details/',views.orderdetails ,name ='orderdetails'),



     



     








     # path('page/',views.shop_page,name ='page'),




]
