from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from . models import Usermodelss, generate_otp,Useraddress
from django.views.decorators.cache import never_cache
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.models import Products,Variant
from category.models import Category
from cart.models import CartItem,order_details

# Create your views here.

@never_cache
def userloginp(request):
    if 'email' in request.session:
        redirect('home')
    if request.method == 'POST':
        email1 = request.POST['email']
        password1 = request.POST['password']
        try:
          user = Usermodelss.objects.get(email=email1,password1=password1)
        except:
            user=None
        
        if user is not None and not user.is_block:
            messages.error(request, 'you account is blocked')
            return redirect(userloginp)
        
        if user is not None:
            if user.is_verified:
                request.session['email']=email1
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
        
       
        
        elif Usermodelss.objects.filter(email=email).exists() :
            messages.error(request, 'This Email  address already exists')
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
    # print(prdts)
    variant = Variant.objects.filter(products_id = id)
    
    return render(request,'single-product.html',{'product':prdts,'variant':variant})

    


def shop(request):
    
    categry = Category.objects.filter(is_listed = True)
    prodts = Products.objects.filter(category__in = categry ,is_listed = True)
   
    return render(request,'shop.html',{'products':prodts,'categorys':categry})


def userlogout(request):
    if 'email' in request.session:
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
  if 'email' in request.session:
    searchh = request.POST.get('S')
    
    prdts = Products.objects.filter(pname__icontains=searchh)
    
    return render(request,'shop.html',{'products':prdts})

def about(request):
    return render(request,'about.html')


# cart section................

def cart(request):
    email1 = request.session['email']
    user = Usermodelss.objects.get(email=email1)
    cartitem = CartItem.objects.filter(user_id=user)
    variant = Variant.objects.all()
    
    for item in cartitem:
        item.total = item.c_quantity * item.Variant_id.v_price
    
    subtotal = sum(item.total for item in cartitem)
    final = subtotal + 45  
    return render(request,'cart.html',{'cartitem':cartitem,'variant':variant,'subtotal':subtotal,'final':final})


def add_cart(request,id):
    
    # try:
    print(id)
    Product = Products.objects.get(id=id)
    
    # except Variant.DoesNotExist:
    #     messages.error(request, "Variant does not exist.")
    #     return redirect('cart')
    # user = request.id
    # user_instance = get_object_or_404(Usermodelss, id=id)
    # print(user_id)
    user = request.session['email']
    # print(user)

    if request.method == 'POST':
        
        user_instance = get_object_or_404(Usermodelss, email=user)
       
        var = request.POST['unit'] 
        

        
        c_quantity = int(request.POST['quantity'])
        print(var,c_quantity)  
        try:   
            var  = Variant.objects.get(products = Product,unit = var)
        except Variant.DoesNotExist:
            messages.error(request, "unit is does not exist.")
            return redirect('shop')
        print(var.id)
       
        cart_item, created = CartItem.objects.get_or_create(
            
            user_id=user_instance,
            Variant_id = var,
            product_id=Product,
            
            defaults={'c_quantity': 1},

            

        )

        if c_quantity < 6:
            
        
            if not created:
                    
                cart_item.c_quantity += int(c_quantity)
                cart_item.c_quantity * cart_item.Variant_id.v_price
                
            else:
                cart_item.c_quantity=1
                cart_item.total =  cart_item.c_quantity * cart_item.Variant_id.v_price
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
    if 'email' in request.session:
        email1 = request.session["email"]
        user = Usermodelss.objects.get(email=email1)
        addres = Useraddress.objects.filter(user_id=user)

   
    
    

    return render(request,'userprofile.html',{'user':user,'addres':addres})






def edituserprofile(request):
    email1 = request.session["email"]
    # print(email1)
    user = Usermodelss.objects.get(email=email1)
    # print(user.email)
    if request.method == 'POST':

        username1 = request.POST['username']    
        phoneno = request.POST['phone']
        
        # print(username1)
        if len(phoneno)!=10:
            messages.error(request, 'Phone number must contains 10 digit')
            return redirect('userprofile')
        
        user.username = username1
        user.phonenumber = phoneno
        user.save()
        
        
        messages.success(request, 'Updated successfully')
        return redirect('userprofile')
    
    return render(request,'userprofile.html',{'user':user})
    


def add_address(request):
   
    
    if request.method == 'POST':
        email1 = request.session["email"]
        user= Usermodelss.objects.get(email=email1)
        add = Useraddress.objects.filter(user_id = user.id).last()
        name = request.POST["name"]
        phonenumber=request.POST["phone"]
        email2 = request.POST["email"]
        country = request.POST["country"]
        state = request.POST["state"]
        address = request.POST["address"]
        pin = request.POST["pin"]
        post = request.POST["post"]
        # print(name)

        if len(phonenumber)==10:
        
            if len(pin)==6:
            
            
                add_addres = Useraddress(
                        user_id=user,
                        Name = name,
                        phone = phonenumber,
                        email = email2,
                        country = country,
                        state = state,
                        address = address,
                        pin = pin,
                        post = post,

                    )
                add_addres.save()
                messages.success(request,"adress successfully added")
                return redirect('userprofile')
            else:
                messages.error(request,"invalid pin number")
                return redirect('userprofile')
            
        else:
            # print(len(phonenumber))
            messages.error(request,"invalid phone number")
            return redirect('userprofile')

    return render(request,"userprofile.html",{'last_addr':add})



def delete_addres(request,id):
    Useraddress.objects.get(id=id).delete()
    return redirect('userprofile')


# check out view....
def checkout(request):
    if 'email' in request.session:
        email1 = request.session["email"]
        user = Usermodelss.objects.get(email=email1)
        cartitem = CartItem.objects.filter(user_id = user)
        if cartitem.exists():

            addres = Useraddress.objects.filter(user_id=user)
        
            variant = Variant.objects.all()
            for item in cartitem:
                item.total = item.c_quantity * item.Variant_id.v_price
            subtotal = sum(item.total for item in cartitem)
            final = subtotal + 45  
            # print(final)
        
        

            return render(request,'checkout.html',{'user':user,'addres':addres,'cartitem':cartitem,'variant':variant,'final':final})
        else:
            messages.error(request,"you can't checkout your cart is empty!...")
            return redirect('shop')


def place_order(request):
    if request.method == 'POST':
        email1 = request.session['email']
        user = Usermodelss.objects.get(email=email1)
        cartitem = CartItem.objects.filter(user_id=user)
        addres = request.POST["selected_address_id"]
        ad = Useraddress.objects.get(id=addres)
        ad1 = ad.id
        for i in cartitem:
            p_order = order_details(
                userid = user,
                pay_method = "cod",
                address = ad,
                total_amount = i.total,
                product_name = i.product_id,
                variant_unit = i.Variant_id,



            )
            p_order.save()
        cartitem.delete()

        return redirect('orderplace')
    else:
        messages.error(request,"oops something error")
        return redirect('checkout')

    



def orderplace(request):

    return render(request,'orderplaced.html')

def orderdetails(request):
    if  'email' in request.session:
        email1 = request.session["email"]
        user = Usermodelss.objects.get(email=email1)
        order = order_details.objects.filter(userid = user)
        # print(order)

    return render(request,'orderdetails.html',{'order':order})