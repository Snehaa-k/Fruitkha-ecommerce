from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from cart.models import Coupon, Orderdetails
from home. models import Usermodelss
from django.utils import timezone
from django.views.decorators.cache import never_cache
from products.models import Variant 
from cart.models import Orderditem
# from fruitkhaprojct.adminpanel.models import adminmodels
# Create your views here.

@never_cache
def adlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            request.session['username']=username 
            login(request,user)
            return redirect('dashbord')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('admnlogin')
    return render(request,'alogin.html')

@never_cache
def dashboard(request):
    if 'username'in request.session:
      return render(request,'ahome.html')
     
    else:
       return redirect(adlogin)
   

@never_cache
def viewusers(request):
    usr=Usermodelss.objects.all()
    current_date = timezone.now()
    if 'username'in request.session:
        return render(request,'veiwusers.html',{'User':usr,'current_date':current_date})
    else:
         return redirect('admnlogin')

def isblock(request,id):
    user = Usermodelss.objects.get(id=id)
    user.is_block = not user.is_block
    user.save()
    # usr = Usermodelss.objects.all()
    # return render(request,'veiwusers.html',{'User':usr})
    return redirect('vusers')

def adminlogout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('admnlogin')


def order_details_admin(request):
    order = Orderdetails.objects.all()
    return render(request,'orderadmin.html',{'order':order})


def order_moredetails(request,id):
    
    orders = Orderdetails.objects.get(id = id)
    orderi = Orderditem.objects.filter(order_id = orders)
    
    subtotal = float(orders.total_amounts)
    
    
        
        
    return render(request,'order-detail.html',{'order':orderi,'subtotal':subtotal})
    

def coupon_list(request):
    coup = Coupon.objects.all()
    return render(request,'coupenlist.html',{'coup':coup})

# add coupen
def addcoupen(request):
    if request.method == 'POST':
        coupenname = request.POST['cname']
        coupenprice = request.POST['cprice']
        coupencode = request.POST['code']
        coupenvalid = request.POST['ctodate']
        coupenex = request.POST['cfromdate']
        if Coupon.objects.filter(code = coupencode).exists():
            messages.success(request, "the coupen code is already exists")
            return redirect("coupon_list")
        else:
            cou = Coupon(
                cop_name = coupenname,
                cop_price = coupenprice,
                code = coupencode,
                from_date = coupenvalid,
                to_date = coupenex,

            )
            cou.save()
            messages.success(request, "your coupen added successfully")
            return redirect('coupon_list')
          
    return render(request,'coupenlist.html')


# edit coupen....
def editcoupen(request,id):
    coup = Coupon.objects.get(id=id)
    if request.method == 'POST':
        coupenname = request.POST['cname']
        coupenprice = request.POST['cprice']
        coupencode = request.POST['code']
        coupenvalid = request.POST['ctodate']
        coupenex = request.POST['cfromdate']
        
        if Coupon.objects.exclude(id=id).filter(code=coupencode).exists():
            messages.success(request, "the coupen code is already exists")
            return redirect("coupon_list")
        else:
            coup.cop_name = coupenname
            coup.cop_price = coupenprice
            coup.code = coupencode
            coup.from_date = coupenvalid
            coup.to_date = coupenex
            coup.save()
            
            messages.success(request, "your coupen added successfully")
            return redirect("coupon_list")
    return render(request,'coupenlist.html',{'coup':coup})


def delete_coupon(request, id):
    if request.method == 'POST':
        Coupon.objects.get(id=id).delete()
        messages.error(request, "coupon deleted succesfully")
        return redirect("coupon_list")

# list coupen
def list_coupen(request, id):
    obj = Coupon.objects.get(id=id)
    obj.is_listed = True
    obj.save()
    return redirect("coupon_list")


# unlist coupen
def un_list_coupen(request, id):
    obj = Coupon.objects.get(id=id)
    obj.is_listed = False
    obj.save()
    return redirect("coupon_list")

def editstatus(request,id):
    stus = Orderditem.objects.get(id = id)
    if request.method == 'POST':
        status = request.POST['status']
        stus.status = status
        stus.save()
        messages.success(request, "your status  is added successfully")
        return redirect("order_details_admin")


    return render(request,'order-detail.html')