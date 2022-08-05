from itertools import product
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os
from .models import *


def homePage(request):
    products = Product.objects.all()
    products=products[::-1]
    return render(request,"index.html",{"Product":products})

def shopPage(request,mc,sc,br):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    if(mc=="All" and sc=="All" and br=="All"):
        products = Product.objects.all()
    elif(mc!="All" and sc=="All" and br=="All"):
        products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc))
    elif(mc=="All" and sc!="All" and br=="All"):
        products = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc))
    elif(mc=="All" and sc=="All" and br!="All"):
        products = Product.objects.filter(brand=Brand.objects.get(name=br))
    elif(mc!="All" and sc!="All" and br=="All"):
        products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc))
    elif(mc!="All" and sc=="All" and br!="All"):
        products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br))    
    elif(mc=="All" and sc!="All" and br!="All"):
        products = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br))      
    else:
        products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br))      
    products=products[::-1]
    return render(request,"shop.html",{"Product":products,
                                       "Maincategory":maincategory,
                                       "Subcategory":subcategory,
                                       "Brand":brand,
                                       "mc":mc,"sc":sc,"br":br                     
                                       })

def login(request):
    if(request.method=='POST'):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            messages.error(request,"Invalid User Name or Password")
    return render(request,"login.html")

def signup(request):
    if(request.method=="POST"):
        actype = request.POST.get('actype')
        if(actype=="seller"):
            u = Seller()
        else:
            u = Buyer()
        u.name = request.POST.get("name")
        u.username = request.POST.get("username")
        u.email = request.POST.get("email")
        u.phone = request.POST.get("phone")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if(password==cpassword):
            try:
                user = User.objects.create_user(username=u.username,password=password,email=u.email)
                user.save()
                u.save()
                return HttpResponseRedirect("/login/")
            except:
                messages.error(request,"User Name already Taken")
                return render(request,"signup.html")    
        else:
            messages.error(request,"Password and Confirm Password does not matched!!!!")
    return render(request,"signup.html")


@login_required(login_url='/login/')
def profilePage(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            seller = Seller.objects.get(username=request.user)
            products = Product.objects.filter(seller=seller)
            products = products[::-1]
            return render(request,"sellerProfile.html",{"User":seller,"Products":products})
        except:
            buyer = Buyer.objects.get(username=request.user)
            wishlist = Wishlist.objects.filter(buyer=buyer)
            return render(request,"buyerProfile.html",{"User":buyer,"Wishlist":wishlist})


@login_required(login_url='/login/')
def updateProfilePage(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            user = Seller.objects.get(username=request.user)
        except:
            user = Buyer.objects.get(username=request.user)
        if(request.method=="POST"):
            user.name=request.POST.get('name')
            user.email=request.POST.get('email')
            user.phone=request.POST.get('phone')
            user.addressline1=request.POST.get('addressline1')
            user.addressline2=request.POST.get('addressline2')
            user.addressline3=request.POST.get('addressline3')
            user.pin=request.POST.get('pin')
            user.city=request.POST.get('city')
            user.state=request.POST.get('state')
            if(request.FILES.get("pic")):
                if(user.pic):
                    os.remove("media/"+str(user.pic))
                user.pic=request.FILES.get('pic')
            user.save()
            return HttpResponseRedirect("/profile/")
    return render(request,"updateProfile.html",{"User":user})

@login_required(login_url='/login/')
def addProduct(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    if(request.method=="POST"):
        p = Product()
        p.name = request.POST.get('name')
        p.maincategory = Maincategory.objects.get(name=request.POST.get('maincategory'))
        p.subcategory = Subcategory.objects.get(name=request.POST.get('subcategory'))
        p.brand = Brand.objects.get(name=request.POST.get('brand'))
        p.baseprice = int(request.POST.get('baseprice'))
        p.discount = int(request.POST.get('discount'))
        p.finalprice = p.baseprice-p.baseprice*p.discount/100
        color=""
        if(request.POST.get("Red")):
            color=color+"Red,"
        if(request.POST.get("Green")):
            color=color+"Green,"
        if(request.POST.get("Yellow")):
            color=color+"Yellow,"
        if(request.POST.get("Pink")):
            color=color+"Pink,"
        if(request.POST.get("White")):
            color=color+"White,"
        if(request.POST.get("Black")):
            color=color+"Black,"
        if(request.POST.get("Blue")):
            color=color+"Blue,"
        if(request.POST.get("Brown")):
            color=color+"Brown,"
        if(request.POST.get("SkyBlue")):
            color=color+"SkyBlue,"
        if(request.POST.get("Orange")):
            color=color+"Orange,"
        if(request.POST.get("Navy")):
            color=color+"Navy,"
        if(request.POST.get("Gray")):
            color=color+"Gray,"
        size=""
        if(request.POST.get("S")):
            size=size+"S,"
        if(request.POST.get("SM")):
            size=size+"SM,"
        if(request.POST.get("M")):
            size=size+"M,"
        if(request.POST.get("L")):
            size=size+"L,"
        if(request.POST.get("XL")):
            size=size+"XL,"
        if(request.POST.get("XXL")):
            size=size+"XXL,"
        if(request.POST.get("XXXL")):
            size=size+"XXXL,"
        p.color=color
        p.size=size
        p.description = request.POST.get('description')
        p.stock = request.POST.get('stock')
        p.pic1 = request.FILES.get('pic1')
        p.pic2 = request.FILES.get('pic2')
        p.pic3 = request.FILES.get('pic3')
        p.pic4 = request.FILES.get('pic4')
        try:
            p.seller = Seller.objects.get(username=request.user)
        except:
            return HttpResponseRedirect("/profile/")
        p.save()
        return HttpResponseRedirect("/profile/")
    return render(request,"addProduct.html",{"Maincategory":maincategory,"Subcategory":subcategory,"Brand":brand})


@login_required(login_url='/login/')
def deleteProduct(request,num):
    try:
        p = Product.objects.get(id=num)
        seller = Seller.objects.get(username=request.user)
        if(p.seller==seller):
            p.delete()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")


@login_required(login_url='/login/')
def editProduct(request,num):
    try:
        p = Product.objects.get(id=num)
        seller = Seller.objects.get(username=request.user)
        if(p.seller==seller):
            maincategory = Maincategory.objects.exclude(name=p.maincategory)
            subcategory = Subcategory.objects.exclude(name=p.subcategory)
            brand = Brand.objects.exclude(name=p.brand)
            if(request.method=="POST"):
                p.name = request.POST.get('name')
                p.maincategory = Maincategory.objects.get(name=request.POST.get('maincategory'))
                p.subcategory = Subcategory.objects.get(name=request.POST.get('subcategory'))
                p.brand = Brand.objects.get(name=request.POST.get('brand'))
                p.baseprice = int(request.POST.get('baseprice'))
                p.discount = int(request.POST.get('discount'))
                p.finalprice = p.baseprice-p.baseprice*p.discount/100
                color=""
                if(request.POST.get("Red")):
                    color=color+"Red,"
                if(request.POST.get("Green")):
                    color=color+"Green,"
                if(request.POST.get("Yellow")):
                    color=color+"Yellow,"
                if(request.POST.get("Pink")):
                    color=color+"Pink,"
                if(request.POST.get("White")):
                    color=color+"White,"
                if(request.POST.get("Black")):
                    color=color+"Black,"
                if(request.POST.get("Blue")):
                    color=color+"Blue,"
                if(request.POST.get("Brown")):
                    color=color+"Brown,"
                if(request.POST.get("SkyBlue")):
                    color=color+"SkyBlue,"
                if(request.POST.get("Orange")):
                    color=color+"Orange,"
                if(request.POST.get("Navy")):
                    color=color+"Navy,"
                if(request.POST.get("Gray")):
                    color=color+"Gray,"
                size=""
                if(request.POST.get("S")):
                    size=size+"S,"
                if(request.POST.get("SM")):
                    size=size+"SM,"
                if(request.POST.get("M")):
                    size=size+"M,"
                if(request.POST.get("L")):
                    size=size+"L,"
                if(request.POST.get("XL")):
                    size=size+"XL,"
                if(request.POST.get("XXL")):
                    size=size+"XXL,"
                if(request.POST.get("XXXL")):
                    size=size+"XXXL,"
                p.color=color
                p.size=size
                p.description = request.POST.get('description')
                p.stock = request.POST.get('stock')
                if(request.FILES.get('pic1')):
                    if(p.pic1):
                        os.remove("media/"+str(p.pic1))
                    p.pic1 = request.FILES.get('pic1')
                if(request.FILES.get('pic2')):
                    if(p.pic2):
                        os.remove("media/"+str(p.pic2))
                    p.pic2 = request.FILES.get('pic2')
                if(request.FILES.get('pic3')):
                    if(p.pic3):
                        os.remove("media/"+str(p.pic3))
                    p.pic3 = request.FILES.get('pic3')
                if(request.FILES.get('pic4')):
                    if(p.pic4):
                        os.remove("media/"+str(p.pic4))    
                    p.pic4 = request.FILES.get('pic4')
                p.save()
                return HttpResponseRedirect("/profile/")
            return render(request,"editProduct.html",{"Product":p,"Maincategory":maincategory,"Subcategory":subcategory,"Brand":brand})
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


def singleProductPage(request,num):
    p = Product.objects.get(id=num)
    color = p.color.split(",")
    color=color[:-1]
    size = p.size.split(",")
    size=size[:-1]
    return render(request,"singleProductPage.html",{"Product":p,"Color":color,"Size":size})


def addToWishlist(request,num):
    try:
        buyer = Buyer.objects.get(username=request.user)
        wishlist = Wishlist.objects.filter(buyer=buyer)
        p = Product.objects.get(id=num)
        flag=False
        for i in wishlist:
            if(i.product==p):
                flag=True
                break
        if(flag==False):
            w = Wishlist()
            w.buyer=buyer
            w.product=p
            w.save()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")

@login_required(login_url='/login/')
def deleteWishlist(request,num):
    try:
        w = Wishlist.objects.get(id=num)
        buyer = Buyer.objects.get(username=request.user)
        if(w.buyer==buyer):
            w.delete()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")