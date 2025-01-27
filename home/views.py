from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import Product,Wishlist,Cart,ContactDetails,Coupon,Billing_Details
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
#from home.cart import countcart
import random

from django.core.validators import EmailValidator


# Create your views here.
def index(request):
    try:
        cart =Cart.objects.filter(user=request.user)
        cartcount = cart.count()
    except:
        cartcount = 0
    products = Product.objects.all()[:3]
    return render(request, 'index.html', {'products': products, 'cartcount':cartcount})
    

def shop(request):
    try:
        cart =Cart.objects.filter(user=request.user)
        cartcount = cart.count()
    except:
        cartcount = 0
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products, 'cartcount':cartcount})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        myuser = auth.authenticate(username=username, password=password)

        if myuser is not None:
            auth.login(request, myuser)
            return redirect ('/')
        else:
            messages.info(request, "Invalid username or password")
    return render(request, 'login.html' )

def userlogout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method== "POST":
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
            request.session['username3']=username
            request.session['email3']=email
            request.session['password13']=password1

            if password1 == password2:
                list = '#$%^&*(){}"<>?,[]+_-=/\|'
                for i in email:
                    if i in list:
                        messages.info(request,"Not a valid email format")
                        return redirect('register')
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username already exist")
                    return redirect('register')
                #elif User.objects.filter(email=email).exists():
                    #messages.info(request, "Email already exist")
                    #return redirect('register')
                elif not username or not email or not password1 or not password2:
                    messages.info(request, "Please fill all the inputs")
                    return redirect('register')
                else:
                    #myuser = User.objects.create_user(username,email,password1)
                    #myuser.save()
                    
                    return render(request, 'home.html')
            else:
                messages.info(request, "Password is not matching")
                return redirect('register')
        
    return render(request, 'registration.html' )

def singleproduct(request,pk):
    try:
        cart =Cart.objects.filter(user=request.user)
        cartcount = cart.count()
    except:
        cartcount = 0   
    product = Product.objects.get(pk=pk)
    return render(request, 'single_product.html', {'product' : product, 'cartcount':cartcount})

@login_required
def myprofile(request):
    cart =Cart.objects.filter(user=request.user)
    cartcount = cart.count()
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        skype = request.POST['skype']
        
        contacts = ContactDetails.objects.filter(user=request.user)

        if contacts.exists():
            for item in contacts:
                item.delete()
                contact = ContactDetails.objects.create(
                    user=request.user,
                    first_name=firstname,
                    second_name=lastname,
                    address=address,
                    mobile_number=phone,
                    email=email,
                    skype=skype
                )
                contact.save()

            return JsonResponse('Contact details updated successfully', safe=False)
        else:
            contact = ContactDetails.objects.create(
                user=request.user,
                first_name=firstname,
                second_name=lastname,
                address=address,
                mobile_number=phone,
                email=email,
                skype=skype
            )
            contact.save()

            return JsonResponse('Contact details updated successfully', safe=False)
        
    items = ContactDetails.objects.filter(user=request.user)
    return render(request, 'myprofile.html', {'items': items, 'cartcount':cartcount})

def deleteprofile(request):
    contacts = ContactDetails.objects.filter(user__username=request.user.username)
    contacts.delete()

    user = request.user
    logout(request)  # Logout the user before deletion
    user.delete()

    return redirect('register')

def wishlist(request):
    print("method", request.method)
    if request.method == "POST":
        print("inside post")
        if request.user.is_authenticated:
            try:
                product = get_object_or_404(Product, id=request.POST.get("product_id"))
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'Product does not exist'})

            if Wishlist.objects.filter(user=request.user, product=product).exists():
                return JsonResponse({"status": "Product already in wishlist"})
            else:
                wishlistitem = Wishlist.objects.create(user=request.user, product=product)
                return JsonResponse({'status': 'Product added successfully', 'wishlist_item_id': wishlistitem.id})

        else:
            return JsonResponse({'status': 'Login to continue'})
        
   
    return redirect('/')

def viewwishlist(request):
    cart =Cart.objects.filter(user=request.user)
    cartcount = cart.count()
    wishlist = Wishlist.objects.filter(user = request.user)
    
    return render(request, 'wishlist.html', {'wishlist':wishlist, 'cartcount':cartcount})

def deletewishlist(request, pk):
    wishitem = Wishlist.objects.get(pk=pk)
    wishitem.delete()
    return redirect('viewwishlist')

def movetocart(request):
    if request.method == "POST":
        print("post")
        wishlist_items = Wishlist.objects.filter(user = request.user)
        
        if wishlist_items.exists():
            for item in wishlist_items:
                existing_cart_item = Cart.objects.filter(user=request.user, product=item.product)
                if existing_cart_item.exists():
                    existing_cart_item = existing_cart_item.first()
                    existing_cart_item.product_qty += 1
                    existing_cart_item.save()
                else:
                    Cart.objects.create(user=request.user, product=item.product, product_qty=1, total_price=item.product.Price)

                item.delete()

            response_data = {'status': 'Items moved to cart successfully', 'reload': True}
            return JsonResponse(response_data)    
        else:
            return JsonResponse({'status': 'No items in wishlist'})
    else:
        pass

def checkout(request):
    if request.method== 'POST':
        amount = 50000
        currency =  "INR"
        client =razorpay.Client(auth=('rzp_test_08T1NafkPtL60N', 'TEhv3y3RplslUhP4joGuap0y'))

        payment = client.order.create({'amount':amount, 'currency': 'INR', 'payment_capture': '1'})

    cart =Cart.objects.filter(user=request.user)
    cartcount = cart.count()
    bill_item = Billing_Details.objects.filter(user=request.user)
    cart= Cart.objects.filter(user=request.user)
    final_price = 0
    cod = "cod"
    upi = "upi"
    for i in cart:
        final_price += i.total_price
    return render(request, 'checkout.html', {'cart':cart, 'final_price':final_price, 'cod':cod, 'upi':upi, 'bill_item':bill_item, 'cartcount': cartcount})

def coupen(request):
    discounted_price = 0 
    cart = Cart.objects.filter(user=request.user)
    final_price = 0
    coupon_items = Coupon.objects.all()
    for item in cart:
        final_price += item.total_price

    if request.method == 'POST':
        code = request.POST['code']
        try:
            Code = Coupon.objects.get(code=code)
            if Code:
                if Code.active == True:
                    discount = Code.discount
                    discounted_price = final_price - discount
                    print(discounted_price)
                else:
                    messages.success(request, "Code is inactive", extra_tags='coupon')
                    return redirect('checkout')   
             
        except:
            print("invalid code")
            messages.success(request, "invalid code", extra_tags='coupon')
            

    return render(request, 'checkout.html', {'cart': cart, 'final_price': final_price, 'dsprice': discounted_price})

def place_order(request):
    cart = Cart.objects.filter(user=request.user)
    if request.method == "POST":
        bill = Billing_Details.objects.filter(user=request.user)
        if bill.exists():
             for item in cart:
                item.delete()
             return redirect('thankyou')
        else:
            messages.info(request, "Please Fill The Shipping Address first", extra_tags="place_order")
            return redirect("checkout")
    else:
        # Handle the case where the request method is not POST if needed
        return HttpResponse("Invalid request method")
    
@csrf_exempt    
def thankyou(request):
    return render(request, 'thankyou.html')

def billing(request):
    final_price = 0
    if request.method == 'POST':

        cart=Cart.objects.filter(user=request.user)
        for i in cart:
            final_price += i.total_price

        fname = request.POST['c_fname']
        lname = request.POST['c_lname']
        address = request.POST['c_address']
        city = request.POST['c_city']
        zip = request.POST['c_postal_zip']
        email = request.POST['c_email_address']
        phone = request.POST['c_phone']

        bill = Billing_Details.objects.filter(user=request.user)

        if bill.exists():
            for item in bill:
                item.delete()

                bill = Billing_Details.objects.create(
                    user= request.user,
                    fname=fname,
                    lname=lname,
                    address=address,
                    city=city,
                    zip=zip,
                    email=email,
                    phone=phone,
                    fullamount=final_price
                )
                bill.save()

                messages.info(request, "Details Updated", extra_tags='bill')
                return redirect('checkout')
        else:
                
            bill = Billing_Details.objects.create(
                user= request.user,
                fname=fname,
                lname=lname,
                address=address,
                city=city,
                zip=zip,
                email=email,
                phone=phone,
                fullamount=final_price
            )
            bill.save()

            messages.info(request, "Details Updated", extra_tags='bill')
            return redirect('checkout')
        
def newaddres(request):
    if request.method == 'POST':

        fname = request.POST['c_diff_fname']
        lname = request.POST['c_diff_lname']
        address = request.POST['c_diff_address']
        city = request.POST['c_diff_city']
        zip = request.POST['c_diff_postal_zip']
        email = request.POST['c_diff_email_address']
        phone = request.POST['c_diff_phone']

        bill = Billing_Details.objects.filter(user=request.user)
        if bill.exists():
            for item in bill:
                item.delete()

                nwads = Billing_Details.objects.create(
                    user= request.user,
                    fname=fname,
                    lname=lname,
                    address=address,
                    city=city,
                    zip=zip,
                    email=email,
                    phone=phone
                )
                nwads.save()
    return redirect('checkout')

#otp
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from .models import OTP

#@login_required
def home(request):
    return render(request, 'home.html')

#@login_required
def send_otp(request):
    recemail = request.session.get('email3')
    if request.method == 'POST':
        #user = request.user
        otp_code = ''.join(random.choice('0123456789') for _ in range(6))
        #OTP.objects.create(user=user, otp=otp_code)
        OTP.objects.create(otp=otp_code)
        # Send OTP via email
        subject = 'Your OTP for Verification'
        message = f'Your OTP is: {otp_code}'
        from_email = settings.DEFAULT_FROM_EMAIL  
        recipient_list = [recemail]
        send_mail(subject, message, from_email, recipient_list)

        return JsonResponse({'message': 'OTP sent successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

#@login_required 
def verify_otp(request):
    username = request.session.get('username3', None)
    email = request.session.get('email3', None)
    password1 = request.session.get('password13', None)

    if request.method == 'POST':
        #user = request.user
        otp_code = request.POST.get('otp')

        #otp_obj = OTP.objects.filter(user=user, otp=otp_code, is_verified=False).first()
        otp_obj = OTP.objects.filter(otp=otp_code, is_verified=False).first()


        if otp_obj:
            otp_obj.is_verified = True
            otp_obj.save()
            myuser = User.objects.create_user(username,email,password1)
            myuser.save()
            return JsonResponse({'message': 'OTP verified successfully'})
        else:
            return JsonResponse({'error': 'Invalid OTP or OTP already verified'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def about(request):
    try:
        cart =Cart.objects.filter(user=request.user)
        cartcount = cart.count()
    except:
        cartcount = 0
    return render(request, 'about.html', {'cartcount':cartcount})
def services(request):
    try:
        cart =Cart.objects.filter(user=request.user)
        cartcount = cart.count()
    except:
        cartcount = 0
    products = Product.objects.all()[:3]
    return render(request, 'services.html', {'products': products, 'cartcount':cartcount})
def blog(request):
    try:
        cart =Cart.objects.filter(user=request.user)
        cartcount = cart.count()
    except:
        cartcount = 0
    return render(request, 'blog.html', {'cartcount':cartcount})
def contact(request):
    try:
        cart =Cart.objects.filter(user=request.user)
        cartcount = cart.count()
    except:
        cartcount = 0
    return render(request, 'contact.html', {'cartcount':cartcount})

        



