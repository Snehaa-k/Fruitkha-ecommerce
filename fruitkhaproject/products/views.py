from pyexpat.errors import messages
from django.shortcuts import render,redirect
from . models import Products
from category.models import Category

# Create your views here.
def productslist(request):
    prodct = Products.objects.all()
    categry = Category.objects.all()
    return render(request,'veiwproducts.html',{'categorys':categry,'product':prodct})



def addproducts(request):
    

    if request.method == 'POST':
        product_name = request.POST['pname']
        image = request.FILES.get('images')
        category_name = request.POST.get('categoryname')
        description = request.POST['description']
        price = request.POST['price']
        instock = request.POST['instock']
       
    
        category_instance, created = Category.objects.get_or_create(category_name = category_name)
       
        prdts = Products(
           
            pname = product_name,
            image = image,
            category = category_instance,
            description = description,
            price = price ,
            in_stock = instock,
            

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
    if request.method == 'POST':
        product_name = request.POST['pname']
        image = request.FILES.get('images')
        category_name = request.POST.get('categoryname')
        description = request.POST['description']
        price = request.POST['price']
        instock = request.POST['instock']
        category_instance, created = Category.objects.get_or_create(category_name = category_name)

        prdts = Products(
        id = id,
        pname = product_name,
        image = image,
        category = category_instance,
        description = description,
        price = price,
        in_stock = instock,

        )

        prdts.save()
        return redirect('productslist')
    return render(request,'veiwproducts.html')

