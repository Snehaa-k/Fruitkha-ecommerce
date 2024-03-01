from datetime import date, timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from . models import Usermodelss, Walletuser, generate_otp,Useraddress,Wishlist
from django.views.decorators.cache import never_cache
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.models import Products,Variant
from category.models import Category
from cart.models import CartItem, Coupon, Orderdetails,Orderditem, Proceedtocheck
from django.db.models import Sum

from django.http import JsonResponse
from django.urls import reverse
from products.models import Productoffer,Categoryoffer
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
            wallet = Walletuser(userid = myuser ,amountt = 0 )
            wallet.save()
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
    prodts = Products.objects.filter(category__in = categry ,is_listed = True,variant__isnull=False).distinct()
    poffer = Productoffer.objects.filter(is_listed = True)
   
    return render(request,'shop.html',{'products':prodts,'categorys':categry,'poffer':poffer})


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
    final = subtotal 
    print(final,"haiii")
    return render(request,'cart.html',{'cartitem':cartitem,'variant':variant,'subtotal':subtotal,'final':final})


# wishlist...............

def add_wishlist(request,id):
    if request.method == 'POST':
        product = Products.objects.get(id=id)
        user = request.session['email']
        obj = Usermodelss.objects.get(email = user)
        var = request.POST['unit'] 
        variant = Variant.objects.get(products = product,unit = var)
        if Wishlist.objects.filter(user_id=obj, product_id=product, vaiant_id=variant).exists():
            messages.error(request, "Product is already in the wishlist!")
            return redirect('singleproduct',product.id)
        wish = Wishlist.objects.create(user_id=obj, product_id=product, vaiant_id=variant)
        wish.save()
        messages.success(request, "Product is added to wishlist")
        return redirect('singleproduct',product.id)

 # show whishlistt.......................
def wishlist(request):
    email1 = request.session['email']
    user = Usermodelss.objects.get(email=email1)
    
    wish = Wishlist.objects.filter(user_id = user)
    
    
    return render(request,'wishlist.html',{'wish':wish})
   
    
def deletewishlist(request,id):
    Wishlist.objects.get(id=id).delete()
    return redirect('wishlist')











def add_cart(request,id):
    
    # try:
   
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
        
        
        obj = Variant.objects.get(products = Product,unit = var)

        cartitem = CartItem.objects.all()
        

        quantity1 = int(request.POST.get('quantity',1))
      
        for item in cartitem:
            item.total = item.c_quantity * item.Variant_id.v_price 
            item.save() 
        

         
       
        
        print(var,quantity1)  
        if  int(quantity1) <= obj.v_quantity: 
            if quantity1 < 6:
                subtotal = int(quantity1) * obj.v_price
                cart_item, created = CartItem.objects.get_or_create( user_id=user_instance,Variant_id = obj,product_id=Product, c_quantity = quantity1,total=subtotal)
                if not created:
                    cart_item.c_quantity = cart_item.c_quantity + 1
                    cart_item.save()
                messages.success(request,"Your Cart is Added successfully..!")
                return redirect('cart')
            else:
                messages.error(request,"quantity is out of limit...")
                return redirect('singleproduct',Product.id)
        else:
            messages.error(request,"story out of stock")
            return redirect('singleproduct',Product.id)
    return render(request,'cart.html')


def delete_cart(request,id):
    CartItem.objects.get(id=id).delete()
    return redirect('cart')


# increase the quantity of cartitem...............
# def increase_cquantity(request):
# #     def quantity_updation(request):
#     if request.method == "POST":
#         cart_id = int(request.POST["cart_id"])
#         action = request.POST["action"]
#         obj = CartItem.objects.get(id=cart_id)
#         pro = Products.objects.get(pname=obj.product_id)
#         unit_qnty = Variant.objects.get(product_id__pname=pro, id=obj.Variant_id.id)
#         if action == "plus":
#             if obj.c_quantity < 5 and obj.c_quantity < unit_qnty.v_quantity:
#                 obj.c_quantity += 1
#                 obj.save()
#             else:
#                 obj.c_quantity = 5

#         else:
#             if obj.c_quantity > 1:
#                 obj.c_quantity -= 1
#                 obj.save()
#             else:
#                 obj.c_quantity = 0
#         return JsonResponse({"status": "alsjdjhfp"})





    
   

def userprofile(request):
    if 'email' in request.session:
        email1 = request.session["email"]
        user = Usermodelss.objects.get(email=email1)
        addres = Useraddress.objects.filter(user_id=user)
        wallet = Walletuser.objects.get(userid=user)
        wallet_amount = wallet.amountt
        


   
    
    

    return render(request,'userprofile.html',{'user':user,'addres':addres,'wallet_amount':wallet_amount})






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
            pro = Proceedtocheck.objects.get(user_id = user)
            
            if pro.is_coupenapplyed:
                
                final = pro.discount_amount

            else:    
                for item in cartitem:
                    item.total = item.c_quantity * item.Variant_id.v_price
                subtotal = sum(item.total for item in cartitem)
                final = subtotal
           
            return render(request,'checkout.html',{'user':user,'addres':addres,'cartitem':cartitem,'variant':variant,'final':final,'pro':pro})
        else:
            messages.error(request,"you can't checkout your cart is empty!...")
            return redirect('shop')
        



#proceedtocheckout
def proceedtocheckout(request):
    email1 = request.session['email']
    user = Usermodelss.objects.get(email = email1)
    userid = user.id
    orderdate = timezone.now().date()
    cart_details = (
        CartItem.objects.select_related("product_id").filter(user_id=user).order_by("-id")
    )
   
   
    # print(subtotal)
    addres = Useraddress.objects.filter(user_id=userid, is_cancelled=False)
    if cart_details.exists():
        for item in cart_details:
            item.total = item.c_quantity * item.Variant_id.v_price
            final= sum(item.total for item in cart_details)
        subtotal = final 
        Proceedtocheck.objects.create(
                user_id=user,
                order_date=orderdate,
                total_amount=subtotal,
                discount_amount=subtotal,
            )
        try:
             Proceedtocheck.objects.get(user_id=user)
        except:
            Proceedtocheck.objects.filter(user_id=user).delete()
            Proceedtocheck.objects.create(
                user_id=user,
                order_date=orderdate,
                total_amount=subtotal,
                discount_amount=subtotal,
            )
            Proceedtocheck.objects.get(user_id=user)
            context1 = {
               
                "cart_details": cart_details,
                "total1": subtotal,
                "addresses": addres,
                "user": user,
               
            }
            return redirect('checkout')
        return render(request,'checkout.html',context1)
    else:
        messages.error(request,"Your cart is empty please add some product..!")
        return redirect('shop')


    










# #place an order section. with cod..............
def place_order(request):
    if request.method == 'POST':
        email1 = request.session['email']
        user = Usermodelss.objects.get(email=email1)
        print("haii")
        userid = user.id
        checkout = Proceedtocheck.objects.get(user_id=user)
        orderdate = timezone.now().date() 
        addres = request.POST["selected_address_id"]
        ad = Useraddress.objects.get(id=addres)
        ad1 = ad.id
        if addres != None:
            order = Orderdetails(
                custom_id = user,
                orders_date=orderdate,
                addr = ad,
                paymt_method = "cod",
                total_amounts = checkout.total_amount,
                discount_amount = checkout.discount_amount,
                coupen_code = checkout.applyed_coupen,
            )
            if checkout.is_coupenapplyed:
                order.coupen_apply = True
            else:
                order.coupen_apply=False
            order.save()
            caritem = CartItem.objects.filter(user_id=userid)
            for i in caritem:
                items = Orderditem(
                    order_id = order,
                    product_n=i.product_id,
                    quantity=i.c_quantity,
                    total_amount=i.total,
                    status="pending",
                    order_number=order.custom_id.id,
                    address_id=ad,
                    ex_deliverey=orderdate + timedelta(days=7),
                    unit = i.Variant_id,


                )
                items.save()
                items.unit.v_quantity = items.unit.v_quantity - items.quantity
                items.unit.save()
                i.delete()
            checkout.delete()
            return redirect('orderplace')
        messages.error(request,"add some address..!")
        return redirect('checkout')
    return render(request,'orderplaced.html',{'orderid':order})








# place an order with razorpay..
def pay_razorpay1(request):
    
    if request.method == 'POST':
        
        email1 = request.session['email']
        user = Usermodelss.objects.get(email=email1)
        checkout = Proceedtocheck.objects.get(user_id=user)
       
        orderdate = timezone.now().date() 
        address_id = request.POST.get("selected_address_id")
        address = Useraddress.objects.get(id=address_id)
        amount = checkout.total_amount
        
        order = Orderdetails.objects.create(
                custom_id=user,
                orders_date=orderdate,
                addr=address,
                paymt_method="razor_pay",
                total_amounts=checkout.total_amount,
                discount_amount = checkout.discount_amount,
                coupen_code = checkout.applyed_coupen,
                
                    )
                    
        cart_items = CartItem.objects.filter(user_id=user)
        
        for cart_item in cart_items:
            Orderditem.objects.create(
                    order_id=order,
                    product_n=cart_item.product_id,
                    quantity=cart_item.c_quantity,
                    total_amount=cart_item.total,
                    status="pending",
                    order_number=order.custom_id.id,
                    address_id=address,
                    ex_deliverey=orderdate + timedelta(days=7),
                    unit=cart_item.Variant_id,
                        ).save()
            cart_item.Variant_id.v_quantity -= cart_item.c_quantity
            cart_item.Variant_id.save()
            cart_item.delete()
        checkout.delete()   
        return JsonResponse({"success": True,"amount":amount, "redirect_url": reverse("orderplace")})

                    
                
            
                
        
    return JsonResponse({"success": False, "redirect_url": "checkout"})
        
    
            
# place an order with Wallet....
def pay_wallet(request):
        email1 = request.session['email']
        user = Usermodelss.objects.get(email=email1)
        if request.method == 'POST':
            
            # email1 = request.session['email']
            # user = Usermodelss.objects.get(email=email1)
            checkout = Proceedtocheck.objects.get(user_id=user)
            
            orderdate = timezone.now().date() 
            address_id = request.POST.get("selected_address_id")
            total = float(request.POST.get("total2"))
           
            
            
            wallet = Walletuser.objects.get(userid=user.id)
            wallet_amt=wallet.amountt
            try:
                if total <= wallet_amt:
                    address = Useraddress.objects.get(id=address_id)
                    order = Orderdetails.objects.create(
                            custom_id=user,
                            orders_date=orderdate,
                            addr=address,
                            paymt_method="wallet",
                            total_amounts=checkout.total_amount,
                            discount_amount = checkout.discount_amount,
                            coupen_code = checkout.applyed_coupen,
                                )
                                
                    cart_items = CartItem.objects.filter(user_id=user)
                    
                    for cart_item in cart_items:
                            Orderditem.objects.create(
                                order_id=order,
                                product_n=cart_item.product_id,
                                quantity=cart_item.c_quantity,
                                total_amount=cart_item.total,
                                status="pending",
                                order_number=order.custom_id.id,
                                address_id=address,
                                ex_deliverey=orderdate + timedelta(days=7),
                                unit=cart_item.Variant_id,
                                    )
                            cart_item.Variant_id.v_quantity -= cart_item.c_quantity
                            cart_item.Variant_id.save()
                            cart_item.delete()
                                
                    checkout.delete()
                    wallet.amountt = wallet.amountt - total
                    wallet.save()
                    return JsonResponse({"success": True, "redirect_url": reverse("orderplace")})
                    
                else:
                    JsonResponse({"success": True, "redirect_url": reverse("checkout")})
                    
            except:                    
                return JsonResponse({"success": True, "redirect_url": reverse("checkout")})
        
        wallet_balance = Walletuser.objects.get(userid=user.id).amountt
        messages.error(request,"Your Wallet has not enough balance")
        return redirect(f"{reverse('checkout')}?wallet_balance={wallet_balance}")
    
    
    
    


    
    



def orderplace(request):
    
    
    return render(request,'orderplaced.html')

def orderdetails(request):
    if  'email' in request.session:
        email1 = request.session["email"]
        user = Usermodelss.objects.get(email=email1)
        userid = user.id
        # ord = Orderdetails.objects.filter(custom_id = userid)
        
        order1 = Orderdetails.objects.filter(custom_id=user).order_by("-id")
                
        # print(order.total_amount)
        # print(order)

    return render(request,'orderdetails.html',{'order':order1})



def moredetails(request,id):
    if  'email' in request.session:
        email1 = request.session["email"]
        Usermodelss.objects.get(email=email1)
        
        orderi = Orderditem.objects.filter(order_id = id)
        
        
    return render(request,'moredetails.html',{'order':orderi})


# cancelling the order......
def cancelorder1(request,id):
    print(id)
    if  'email' in request.session:
        email1 = request.session["email"]
        user =  Usermodelss.objects.get(email=email1)
        usr = user.id
        print(usr)
        orderi = Orderditem.objects.get(id=id)
        
        variant = Variant.objects.get(products = orderi.product_n ,unit = orderi.unit.unit)
        print(variant.products)
        
        variant.v_quantity = variant.v_quantity + orderi.quantity
        variant.save()
        return_amount =  orderi.total_amount
        print(return_amount)
        orderi.status = "cancelled"
        orderi.save()
        if orderi.order_id.paymt_method == "razor_pay" or orderi.order_id.paymt_method == "wallet":
            wallet1 = Walletuser.objects.get(userid = user.id )
            # print(type(wallet1.amountt))

            
            wallet1.amountt=wallet1.amountt + return_amount
            wallet1.save()

            
        messages.success(request,"order cancelled successfully")
        return redirect('orderdetails')


# apply a coupen....
def coupenapply(request):
    if request.method == "POST":
        email1 = request.session['email']
        user = Usermodelss.objects.get(email=email1)
        
        appcoup = request.POST.get('coupon_code')
        pro = Proceedtocheck.objects.get(user_id = user)
        
        try:
            coupen = Coupon.objects.get(code = appcoup)
            if coupen.to_date < date.today():
                return JsonResponse({'success': False, 'message': 'Coupon has expired'})
            if Orderdetails.objects.filter(custom_id = user , coupen_code = coupen ).exists():
                return JsonResponse({'success': False, 'message': 'Coupon already applied'})
            if coupen.is_listed:
                pro.discount_amount = pro.total_amount - coupen.cop_price
                if pro.discount_amount < 0:
                    pro.discount_amount = 0
                    pro.applyed_coupen = coupen
                    pro.is_coupenapplyed = True
                    pro.save()

                pro.applyed_coupen = coupen
                pro.is_coupenapplyed= True
                pro.save()
            
                JsonResponse({'success': False, 'message': 'Coupon applied succesfully'}) 
                return redirect('checkout')
            else:
                JsonResponse({'success': False, 'message': "you can't apply this coupon"}) 

           
        except Coupon.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Coupon Doesnot Exists'})
    return render(request,'checkout.html')

        
            








    
   

   

# change password section..........
def changepassword(request):
    email1 = request.session['email']
    user = Usermodelss.objects.get(email = email1)
    if request.method == 'POST':
        new_pass = request.POST['newPassword']
        new_pass1 = request.POST['confirmPassword']
        user.password1 = new_pass
        if new_pass == new_pass1:
            user.save()
            return redirect('userlog')
        else:
            messages.error(request,"password does not match")
            return redirect('changepassword')



    return render(request,'changepassword.html')


#password confirmation...........
def old_pass_confirm(request):
    email1 = request.session['email']
    user = Usermodelss.objects.get(email = email1)
    # print(oldpass)
    if request.method == "POST":
        oldpass = user.password1
        entered_p = request.POST['confirmPassword']
        # print("hai",entered_p)
        if entered_p != str(oldpass):
           messages.error(request," Invalid Password ")
           return redirect('old_pass_confirm')
        else:
            return redirect("changepassword")
    return render(request,'paaswordentering.html')


# cancel the order..............






def add_addr_checkout(request):
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
                return redirect('checkout')
            else:
                messages.error(request,"invalid pin number")
                return redirect('checkout')
            
        else:
            # print(len(phonenumber))
            messages.error(request,"invalid phone number")
            return redirect('checkout')

    return render(request,"checkout.html",{'last_addr':add})










def contact(request):
    return render(request,'contact.html')