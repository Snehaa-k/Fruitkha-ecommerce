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






     # path('page/',views.shop_page,name ='page'),




]
