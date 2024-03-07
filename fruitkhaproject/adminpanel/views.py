from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from cart.models import CartItem, Coupon, Orderdetails
from home. models import Usermodelss
from django.utils import timezone
from django.views.decorators.cache import never_cache
from products.models import Variant,Products
from cart.models import Orderditem
from products.models import Productoffer,Categoryoffer
from category.models import Category
from django.db.models import Q ,Sum,Count
# from fruitkhaprojct.adminpanel.models import adminmodels
# Create your views here.

@never_cache
def adlogin(request):
    if 'email' in request.session:
        return redirect('error404')
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
    if 'email' in request.session:
        return redirect('error404')
    if 'username'in request.session:

        total = Orderdetails.objects.aggregate(total_amount = Sum('discount_amount'))['total_amount']
        if total != None:
            total_earnings = total
            ear_per = total_earnings/100
        else:
            total_earnings=0
        
        
        total_c = Usermodelss.objects.aggregate(count_u = Count('id') )['count_u']
        if total_c != None:
            total_coustomers = total_c
            c_per = total_coustomers/100
           
        else:
            total_coustomers=0
       
        total_o = Orderdetails.objects.aggregate(count_o = Count('id'))['count_o']
        if total_o != None:
            total_orders = total_o
            or_pec = total_orders/100
           
        else:
            total_orders=0
        
        total_cop = Coupon.objects.aggregate(count_cop = Count('id'))['count_cop']
        if total_cop != None:
            total_coup = total_cop
            cop_pec = total_coup/100
           
        else:
            total_coup=0
       
       
        return render(request,'ahome.html',{'total_e':total_earnings,'total_user':total_coustomers,'total_orders':total_orders,'ear_per':ear_per,'c_per':c_per,'or_pec':or_pec,'total_coup':total_coup,'cop_pec':cop_pec})
      
     
    else:
       return redirect(adlogin)
    

@never_cache
def viewusers(request):
    if 'email' in request.session:
        return redirect('error404')
    usr=Usermodelss.objects.all()
    current_date = timezone.now()
    if 'username'in request.session:
        return render(request,'veiwusers.html',{'User':usr,'current_date':current_date})
    else:
         return redirect('admnlogin')

def isblock(request,id):
    if 'email' in request.session:
        return redirect('error404')
    user = Usermodelss.objects.get(id=id)
    user.is_block = not user.is_block
    user.save()
    # usr = Usermodelss.objects.all()
    # return render(request,'veiwusers.html',{'User':usr})
    return redirect('vusers')

def adminlogout(request):
    if 'email' in request.session:
        return redirect('error404')
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
    if 'email' in request.session:
        return redirect('error404')
    coup = Coupon.objects.all()
    return render(request,'coupenlist.html',{'coup':coup})

# add coupen
def addcoupen(request):
    if 'email' in request.session:
        return redirect('error404')
    
    if request.method == 'POST':
        coupenname = request.POST['cname']
        coupenprice = request.POST['cprice']
        coupencode = request.POST['code']
        coupenvalid = request.POST['ctodate']
        coupenex = request.POST['cfromdate']
        
        if  coupenname.strip() == '' or  coupencode.strip() == '' :
            messages.error(request,"Enter valid coupen")
            return redirect('coupon_list')
        else:

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
    if 'email' in request.session:
        return redirect('error404')
    coup = Coupon.objects.get(id=id)
    if request.method == 'POST':
        coupenname = request.POST['cname']
        coupenprice = request.POST['cprice']
        coupencode = request.POST['code']
        coupenvalid = request.POST['ctodate']
        coupenex = request.POST['cfromdate']
        
        if  coupenname.strip() == '' or coupencode.strip() == '':
            messages.error(request,"Enter valid coupen")
            return redirect('coupon_list')
        else:
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


def productoffer(request):
    products = Products.objects.filter(is_listed = True)
    offer = Productoffer.objects.all()
    
    return render(request,'productoffer.html',{'product':products,'offer':offer})


def addproductoffer(request):
    if 'email' in request.session:
        return redirect('error404')
    products = Products.objects.filter(is_listed = True)
   
    if request.method == 'POST':
       
        product1 = request.POST['prodt']
        perc = int(request.POST['perc'])
        # offer = Productoffer.objects.filter(product_id = product)
        if Productoffer.objects.filter(product_id = product1).exists():

            messages.success(request, "the offer for this product is already exists")
            return redirect("productoffer")

        if perc <= 100 and perc >= 0:
            produc = Products.objects.get(id=product1)
            Productoffer.objects.create(product_id = produc,percentage = perc)
            messages.success(request,"product offer added successffully..!")
            return redirect('productoffer')
        messages.success(request, "the percentage should between 0 and 100")
        return redirect("productoffer")        
       
    return render(request,'productoffer.html',{'product':products})

def list_poffer(request, id):
    p = Productoffer.objects.get(id=id)
    p.is_listed = True
    p.save()
    return redirect("productoffer")

def ulist_poffer(request, id):
    p = Productoffer.objects.get(id=id)
    p.is_listed = False
    p.save()
    return redirect("productoffer")

def editproductoffer(request,id):
    if 'email' in request.session:
        return redirect('error404')
    offer = Productoffer.objects.get(id = id)
    if request.method == 'POST':
        product1 = request.POST['prodt']
        perc = int(request.POST['perc'])
        if Productoffer.objects.filter(product_id = product1).exists():

            messages.success(request, "the offer for this product is already exists")
            return redirect("productoffer") 
        if perc <= 100 and perc >= 0:
            produc = Products.objects.get(id=product1)
            offer.product_id = produc
            offer.percentage = perc
            offer.save()
            messages.success(request,"product offer added successffully..!")
            return redirect('productoffer')
        messages.success(request, "the percentage should between 0 and 100")
        return redirect("productoffer") 
    
    return render(request,'productoffer.html',{'offer':offer})

def categoryoffer(request):
    if 'email' in request.session:
        return redirect('error404')
    category = Category.objects.filter(is_listed = True)
    offerc = Categoryoffer.objects.all()
    return render(request,'categoryloffer.html',{'category':category,'offerc':offerc})

def addcategoryoffer(request):
    if 'email' in request.session:
        return redirect('error404')
    if request.method == "POST":
        category = request.POST['cat']
        perct = int(request.POST['perc'])
        
        if Categoryoffer.objects.filter(category_id =category ).exists():

            messages.success(request, "the offer for this category is already exists")
            return redirect("categoryoffer")
        else:

            if perct <= 100 and perct >= 0:
                cat = Category.objects.get(id=category)
                Categoryoffer.objects.create(category_id = cat,percentage = perct)
                messages.success(request,"product offer added successffully..!")
                return redirect('categoryoffer')
            messages.success(request, "the percentage should between 0 and 100")
            return redirect("categoryoffer") 

    return render(request,'categoryloffer.html')

def editcategoryoffer(request,id):
    if 'email' in request.session:
        return redirect('error404')
    cat = Categoryoffer.objects.get(id = id)
    if request.method == "POST":
        category = request.POST['cat']
        perct = int(request.POST['perc'])
        
        preselect = cat.category_id
        print(preselect)
        # # if Categoryoffer.objects.filter(category_id =category ).exists():

        #     messages.success(request, "the offer for this category is already exists")
        #     return redirect("categoryoffer")

        if perct <= 100 and perct >= 0:
            cate = Category.objects.get(id=category)
            
            cat.category_id = cate
            cat.percentage = perct
           
            cat.save()
            messages.success(request,"category offer added successffully..!")
            return redirect('categoryoffer')
        messages.success(request, "the percentage should between 0 and 100")
        return redirect("categoryoffer") 

    return render(request,'categoryloffer.html',{'category':cat,'preselect':preselect})


def list_coffer(request, id):
    c = Categoryoffer.objects.get(id=id)
    c.is_listed = True
    c.save()
    return redirect("categoryoffer")

def ulist_coffer(request, id):
    c = Categoryoffer.objects.get(id=id)
    c.is_listed = False
    c.save()
    return redirect("categoryoffer")

def error404(request):
    
    return render(request,'404.html')


def salesreport(request):
    if request.method == "POST":
        start = request.POST["startdate"]
        end = request.POST["enddate"]
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        if end_date > start_date:
            orderi = Orderditem.objects.filter(
                Q (status="Delivered") & Q (order_id__orders_date__range=[start, end])
            )
        else:
            messages.error(request, "Enter valid date..!")
            return redirect("dashbord")
    return render(request, "salesreport.html", {"orders": orderi})

def delete_productoff(request, id):
    if request.method == 'POST':
        Productoffer.objects.get(id=id).delete()
        messages.error(request, "offer deleted succesfully")
        return redirect("productoffer")

def delete_catoff(request,id):
    if request.method == 'POST':
        Categoryoffer.objects.get(id=id).delete()
        messages.error(request, "offer deleted succesfully")
        return redirect("categoryoffer")

