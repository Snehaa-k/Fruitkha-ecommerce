from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from . models import Usermodelss, generate_otp
from django.views.decorators.cache import never_cache
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.models import Products,Variant
from category.models import Category
from cart.models import CartItem
from django.db.models import Func,F

# Create your views here.

@never_cache
def userloginp(request):
    if 'username' in request.session:
        redirect('home')
    if request.method == 'POST':
        username1 = request.POST['username']
        password1 = request.POST['password']
        try:
          user = Usermodelss.objects.get(username=username1,password1=password1)
        except:
            user=None
        
        if user is not None and not user.is_block:
            messages.error(request, 'you account is blocked')
            return redirect(userloginp)
        
        if user is not None:
            if user.is_verified:
                request.session['username']=username1
                return render(request,'home.html')
            else:
                generate_otp(user)
                return redirect('otpver',user.id)

        else:
            messages.error(request, 'Invalid username or password')
            return redirect(userloginp)
        
       
    return render(request,'userloginpage.html')





def usersignupa(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phoneno = request.POST['phonenumber']
        Pass1= request.POST['password1']
        pass2= request.POST['password2']
        if len(phoneno)!=10:
            messages.error(request, 'Phone number must contains 10 digit')
            return render(request, 'usersignuppage.html')
        if Pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'usersignuppage.html')
        
        elif Usermodelss.objects.filter(username=username).exists():
            messages.error(request,' username is already exists')
            return render(request,'usersignuppage.html')
        
        elif Usermodelss.objects.filter(email=email).exists() :
            messages.error(request, 'This Email or username address already exists')
            return render(request,'usersignuppage.html')
        else:
            myuser = Usermodelss(username=username,email=email,phonenumber=phoneno,password1=Pass1,password2=pass2)
            myuser.save()
            return redirect('otpver',myuser.id)
    return render(request,'usersignuppage.html')
    # return render(request,'usersignuppage.html')

@never_cache
def otpver(request,id):
    user = Usermodelss.objects.get(id=id)
    if request.method == 'POST':
        otpverification=request.POST['otpverification']
        enter_otp = user.otp
        if otpverification == enter_otp:
            user.is_verified=True
            user.save()
            return redirect('userlog')
            
            
        else:
            messages.error(request, 'OTP you entered is not correct')
            return redirect('otpver',id)
            

    return render(request,'otp.html',{"id":id})  


def home(request):
    return render(request, 'home.html')

def singleproduct(request,id):
    prdts = Products.objects.get(id = id)
    print(prdts)
    variant = Variant.objects.get(products_id = id)
    
    return render(request,'single-product.html',{'product':prdts,'variant':variant})

    


def shop(request):
    
    categry = Category.objects.filter(is_listed = True)
    prodts = Products.objects.filter(category__in = categry ,is_listed = True)
   
    return render(request,'shop.html',{'products':prodts,'categorys':categry})


def userlogout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('userlog')




# def Delete(request,id):
#     prdts=Products.objects.filter(id=id).delete()



# def shop_page(request):
#     prodts = Products.objects.all()
#     items_per_page = 6
#     page = request.GET.get('page', 1)
    
#     paginator = Paginator(prodts, items_per_page)
    
#     try:
#         products = paginator.page(page)
#     except EmptyPage:
#         products = paginator.page(paginator.num_pages)

#     return render(request, 'shop.html', {'products': products})


def searchh(request):
  if 'username' in request.session:
    searchh = request.POST.get('S')
    
    prdts = Products.objects.filter(pname__icontains=searchh)
    
    return render(request,'shop.html',{'products':prdts})

def about(request):
    return render(request,'about.html')


# cart section................

def cart(request):
    cartitem = CartItem.objects.all()
    variant = Variant.objects.all()
   
    
    
    return render(request,'cart.html',{'cartitem':cartitem,'variant':variant})


def add_cart(request,id):
    
    variant = Variant.objects.get(id=id)
    # user = request.id
    # user_instance = get_object_or_404(Usermodelss, id=id)
    # print(user_id)
    user = request.session['username']
    print(user)

    if request.method == 'POST':
        
        user_instance = get_object_or_404(Usermodelss, username=user)
        
        
        c_quantity = int(request.POST['quantity'])
        
       
        cart_item, created = CartItem.objects.get_or_create(
            
            user_id=user_instance,
            Variant_id = variant,
            product_id=variant.products,
            defaults={'c_quantity': 1}
            

        )

        if c_quantity < 6:
            
        
            if not created:
                    
                cart_item.c_quantity += int(c_quantity)
                
            else:
                cart_item.c_quantity=1
            
            cart_item.save()
            
            return redirect('cart')
        
        else:
            messages.error(request,"quantity is out of limit...")
            return redirect('cart')
    
    return render(request,'cart.html')


def delete_cart(request,id):
    CartItem.objects.get(id=id).delete()
    return redirect('cart')



def userprofile(request):

    return render(request,'userprofile.html')
