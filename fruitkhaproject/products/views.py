import os
from django.contrib import messages
from django.shortcuts import render,redirect
from . models import Products
from category.models import Category
from . models import Variant

# Create your views here.
def productslist(request):
    prdts = Products.objects.all()
    categry = Category.objects.all()
    variant = Variant.objects.all()
    return render(request,'veiwproducts.html',{'categorys':categry,'product':prdts,'variant':variant})



def addproducts(request):
    if 'email' in request.session:
        return redirect('error404')
    if request.method == 'POST':
        product_name = request.POST['pname']
        image = request.FILES.get('images')
        imagea = request.FILES.get('imagesa')
        imageb = request.FILES.get('imagesb')
        category_name = request.POST.get('categoryname')
        description = request.POST['description']
        category_instance, created = Category.objects.get_or_create(category_name = category_name)
        if  product_name.strip() == '' or  description.strip() == '' :
            messages.error(request,"Enter valid Products")
            return redirect('productslist')
       
        prdts = Products(
           
            pname = product_name,
            image = image,
            category = category_instance,
            description = description,
            imagea = imagea,
            imageb = imageb,
            

        )
       
        prdts.save()

        return redirect('productslist')
    return render(request,'veiwproducts.html',{'product':prdts})


def is_listed(request,id):
    prdts = Products.objects.get(id=id)
    prdts.is_listed = not prdts.is_listed
    prdts.save()
    prdts = Products.objects.all()
    return redirect('productslist')


def editproducts(request):
    prdts = Products.objects.get(id=id)
   
    return render(request,'veiwproducts.html',{'product':prdts})


def updateproduct(request,id):
    if 'email' in request.session:
        return redirect('error404')
    prdts = Products.objects.select_related("category").get(id=id)
    if request.method == 'POST':
        product_name = request.POST['pname']
        image = request.FILES["images"] if "images" in request.FILES else None
        imagea = request.FILES["imagesa"] if "imagesa" in request.FILES else None
        imageb = request.FILES["imagesb"] if "imagesb" in request.FILES else None
        
        category_name = request.POST.get('categoryname')
        description = request.POST['description']
       
        category_instance, created = Category.objects.get_or_create(category_name = category_name)
        prdts.pname = product_name
        prdts.image = image if image else prdts.image
        prdts.imagea = imagea if imagea else prdts.imagea
        prdts.imageb = imageb if imageb else prdts.imageb
        prdts.category = category_instance
        prdts.description = description

        try:
            prdts.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('productslist')
        except Exception as e:
            messages.error(request, f'Error updating product: {e}')
    return render(request,'veiwproducts.html')



# variant section........................
def add_variant(request,id):
    if 'email' in request.session:
        return redirect('error404')
    prdts = Products.objects.get(id=id)
    
    if request.method == 'POST':
        unit = request.POST['unit']
        price = request.POST['price']
        quantity = request.POST['quantity']
        if not Variant.objects.filter(unit=unit, products_id=id).exists():
            variant = Variant(
                products = prdts,
                unit = unit,
                v_price = price,
                v_quantity = quantity,

            )
            variant.save()
            messages.error(request, "variant added successfully")
            return redirect('productslist')
        else:
            messages.error(request, "the unit is already added so just update it")
            return redirect('productslist')
    return render(request,'veiwproducts.html')




def edit_variant_modal(request, id):
    if 'email' in request.session:
        return redirect('error404')
    product = Products.objects.get(id=id)
    variant = Variant.objects.filter(products=product).first()
    if request.method == 'POST':
        quantity = request.POST['quantity']
        price = request.POST['price']
        if quantity is not None and price is not None:
           
            variant.v_quantity = quantity
            variant.v_price=price
            variant.save()
            messages.success(request, "Quantity and price updated successfully")
            return redirect('productslist')
        
        else:
            messages.error(request, "Quantity  and price is required")
            return redirect('productslist')
    return render(request,'veiwproducts.html',{'variant':variant})


