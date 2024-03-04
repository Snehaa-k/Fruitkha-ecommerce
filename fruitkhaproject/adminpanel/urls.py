from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.adlogin,name='admnlogin'),
    path('home/',views.dashboard,name='dashbord'),
    path('vusers/',views.viewusers,name='vusers'),
    path('block/<str:id>',views.isblock,name='userblock'),
    path('logout/',views.adminlogout,name='adminlogout'),
    path('orderadmin/',views.order_details_admin,name='order_details_admin'),
    path('order_moredetails/<str:id>',views.order_moredetails,name='order_moredetails'),
    path('coupen/',views.coupon_list,name='coupon_list'),
    path('addcoupen/',views.addcoupen,name='addcoupen'),
    path('editcoupen/<str:id>',views.editcoupen,name='editcoupen'),
    path('delete_coupon/<str:id>',views.delete_coupon,name='delete_coupon'),
    path('list_coupen/<str:id>',views.list_coupen,name='list_coupen'),
    path('un_list_coupen/<str:id>',views.un_list_coupen,name='un_list_coupen'),
    path('editstatus/<str:id>',views.editstatus,name='editstatus'),
    path('productoffer/',views.productoffer,name='productoffer'),
    path('addproductoffer/',views.addproductoffer,name='addproductoffer'),
    path('listed/<str:id>',views.list_poffer,name='listed'),
    path('unlisted/<str:id>',views.ulist_poffer,name='unlisted'),
    path('editoffer/<str:id>',views.editproductoffer,name='editproductoffer'),
    path('categoryoffer/',views.categoryoffer,name='categoryoffer'),
    path('addcategoryoffer/',views.addcategoryoffer,name='addcategoryoffer'),
    path('editcategoryoffer/<str:id>',views.editcategoryoffer,name='editcategoryoffer'),
    path('list_coffer/<str:id>',views.list_coffer,name='list_coffer'),
    path('ulist_coffer/<str:id>',views.ulist_coffer,name='ulist_coffer'),
    path('error/',views.error404,name='error404'),
    path('salesreport/',views.salesreport,name='salesreport'),
    path('delete_productoff/<str:id>',views.delete_productoff,name='delete_productoff'),
    path('delete_catoff/<str:id>',views.delete_catoff,name='delete_catoff'),















  







    
    


]
