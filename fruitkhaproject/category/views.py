from django.shortcuts import render,redirect
from . models import Category

# Create your views here.
def category(request):
    categry = Category.objects.all()
    
    return render(request,'categorylist.html',{'categorys':categry})
   
   

def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        image = request.FILES.get('images')
        categry = Category(
             category_name = category_name,
             image = image,
        )
        categry.save()
        return redirect('category')
        

    return render(request,'categorylist.html')

def editcategory(request):
    categry = Category.objects.all()
    return render(request,'categorylist.html',{'categorys':categry})



def updatecategory(request,id):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        image = request.FILES.get('images')
        categry = Category(
            id=id,
            category_name = category_name,
            image = image,
        )
        categry.save()
        return redirect('category')
    return render(request,'categorylist.html')

def category_is_listed(request,id):
    categry = Category.objects.get(id=id)
    categry.is_listed = not categry.is_listed
    categry.save()
    categry = Category.objects.all()
    return redirect('category')