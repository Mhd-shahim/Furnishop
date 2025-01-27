from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth,User
from django.contrib.auth import login
from django.contrib import messages
from home.models import Product,Category,Coupon,Billing_Details
from home.forms import ProductForm,CategoryForm,CouponForm


# Create your views here.

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    elif request.method == 'POST':
        username =request.POST['username']
        password =request.POST['password']
        myuser = auth.authenticate(username=username, password=password)

        if myuser and myuser.is_superuser:
            login(request, myuser)
            request.session['username'] = username

            return redirect('dashboard')
        else:
            messages.info(request, "Invalid username or password ")
            return redirect('admin_login')
    else:
        return render(request, 'admin_login.html')
    
def admin_logout(request):
    auth.logout(request)
    return redirect('admin_login')

def admin_dashboard(request):
    if 'username' in request.session:
        return render(request, 'Furniadmin.html')
    else:
        return redirect('admin_login')

def user_list(request):
    if 'username' in request.session:
        myuser = User.objects.all()
        return render(request, 'userlist.html', {'myuser': myuser})
    else:
        return redirect('admin_login')

def delete(request,pk):
     if 'username' in request.session:
        user = User.objects.get(pk=pk)
        user.delete()
        myuser = User.objects.all()
        #return render(request, 'userlist.html', {'myuser': myuser})
        return redirect('userlist')
     else:
         return redirect('admin_login')

def add_product(request):
    if 'username' in request.session:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return redirect('viewproduct')
        else:
            form = ProductForm()
            return render(request, 'Add_product.html', {'form': form})
    else:
        return redirect('admin_login')
    
def deleteprod(request,pk):
     if 'username' in request.session:
        products = Product.objects.get(pk=pk)
        products.delete()
        products = Product.objects.all()
        #return render(request, 'viewproduct.html', {'products': products})
        return redirect('viewproduct')
     else:
         return redirect('admin_login')


def editproduct(request,pk):
    if 'username' in request.session:
        products = Product.objects.get(pk=pk)
        if request.method == 'POST':
            prod_name = request.POST.get('name')
            prod_image = request.POST.get('img')
            prod_price = request.POST.get('price')
            prod_category = request.POST.get('myfield')

            products.name = prod_name
            products.img = prod_image
            products.price = prod_price
            products.my_field = prod_category

            form = ProductForm(request.POST, request.FILES, instance=products)
            if form.is_valid():
                form.save()
                return redirect('viewproduct')
        
        else:
            form = ProductForm(instance=products)
            return render(request, 'Add_product.html', {'form':form})
    else:
        return redirect('admin_login')
    
def view_product(request):
    if 'username' in request.session:
        products = Product.objects.all()
        return render(request, 'viewproduct.html', {'products':products})
    else:
        return redirect('admin_login')

def categories(request):
    if 'username' in request.session:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('categories')
        else:
            form = CategoryForm()
            categories = Category.objects.all()
            return render(request, 'categories.html', {'form' : form, 'categories':categories})
    else:
         return redirect('admin_login')
    
def deletecat(request,pk):
     if 'username' in request.session:
        categories = Category.objects.get(pk=pk)
        categories.delete()
        categories = Category.objects.all()
        form = CategoryForm()
        #return render(request, 'categories.html', {'form' : form, 'categories':categories})
        return redirect('categories')
     else:
         return redirect('admin_login')
def Couponcodes(request):
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("form is not valid")
        return redirect('adcoupon')
    else:
        form = CouponForm()
        coupons = Coupon.objects.all()
        return render(request, 'coupen.html', {'form': form, 'coupons':coupons})
    
def deletecoupon(request,pk):
     if 'username' in request.session:
        coupons = Coupon.objects.get(pk=pk)
        coupons.delete()
        return redirect('adcoupon')
     else:
         return redirect('admin_login')
     
def editcoupon(request, pk):
    coupon = Coupon.objects.get(pk=pk)

    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('adcoupon')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'editcoupon.html', {'form': form, 'coupon': coupon})

def order_management(request):
    orders = Billing_Details.objects.all()
    return render(request, 'Order_management.html', {'orders' : orders})
