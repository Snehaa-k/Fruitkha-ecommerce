from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.adlogin,name='admnlogin'),
    path('home/',views.dashboard,name='dashbord'),
    path('vusers/',views.viewusers,name='vusers'),
    path('block/<str:id>',views.isblock,name='userblock'),
    path('logout/',views.adminlogout,name='adminlogout'),
    
    


]
