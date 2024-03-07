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
        # price = request.POST['price']
        # instock = request.POST['instock']
       
    
        category_instance, created = Category.objects.get_or_create(category_name = category_name)
       
        prdts = Products(
           
            pname = product_name,
            image = image,
            category = category_instance,
            description = description,
            # price = price ,
            # in_stock = instock,
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
    if request.method == 'POST':
        product_name = request.POST['pname']
        image = request.FILES.get('images')
        imagea = request.FILES.get('imagesa')
        imageb = request.FILES.get('imagesb')
        category_name = request.POST.get('categoryname')
        description = request.POST['description']
        # price = request.POST['price']
        # instock = request.POST['instock']
        category_instance, created = Category.objects.get_or_create(category_name = category_name)
       
        # delete_image = request.POST.get('delete_image')
        # if delete_image:
        #     Products.image.delete()
        # image = request.FILES.get('images')
        # imagea = request.FILES.get('imagesa')
        # imageb = request.FILES.get('imagesb')
        
        

        prdts = Products(
        id = id,
        pname = product_name,
        image = image,
        category = category_instance,
        description = description,
        # price = price,
        # in_stock = instock,
        imagea = imagea,
        imageb = imageb,

        )


        prdts.save()
        return redirect('productslist')
    return render(request,'veiwproducts.html')

# variant section........................

def add_variant(request,id):
    if 'email' in request.session:
        return redirect('error404')
    prdts = Products.objects.get(id=id)
    # print(id)
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
    
    # print("haii")
    if request.method == 'POST':
        quantity = request.POST['quantity']
        price = request.POST['price']
        # print(quantity)
        # print(price)
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


