from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from home. models import Usermodelss
from django.utils import timezone
from django.views.decorators.cache import never_cache
from products.models import Variant 
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

