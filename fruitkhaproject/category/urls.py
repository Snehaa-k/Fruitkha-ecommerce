from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.category, name="category"),
    path("add/", views.addcategory, name="addcategory"),
    path("edit/", views.editcategory, name="editcategory"),
    path("update/<str:id>/", views.updatecategory, name="updatecategory"),
    path("list/<str:id>", views.category_is_listed, name="list"),
]
