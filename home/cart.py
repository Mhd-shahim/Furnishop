from itertools import product
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import Product,Cart
from django.contrib.auth.models import User

def addtocart(request):
    print("method",request.method)
    if request.method == "POST":
        print("inside post")
        if request.user.is_authenticated:
            prod_id = request.POST.get("product_id")
            prod_check = Product.objects.get(id=prod_id)
            
            if(prod_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    print('product add')
                    return JsonResponse({"status":"Product already in cart"})
                else:
                    prod_qty = int(request.POST.get("product_qty"))
                    
                    if prod_check.Quantity == 0:
                        return JsonResponse({'status': "Product is out of stock"})

                    elif prod_check.Quantity >= prod_qty:
                        if prod_qty == 0:
                            
                            Cart.objects.create(user=request.user, product_id=prod_id, product_qty=1, total_price=prod_check.Price)
                            return JsonResponse({"status":"Product added successfully"})
                        else:
                            total_price = prod_check.Price * prod_qty
                            Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty, total_price=total_price)
                            return JsonResponse({"status":"Product added successfully"})
                    else:
                        return JsonResponse({'status': "Only " + str(prod_check.Quantity) + " quantity available"})

            else:
               return JsonResponse({'status': "No such product"})

        else:
            return JsonResponse({'status': "Login to continue"})
    print('outside post')
    return redirect('/')

def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    countcart = cart.count()
    print(countcart)
    final_price = 0
    for i in cart:
        final_price += i.total_price
    return render(request, 'cart.html', {'cart': cart, 'final_price': final_price, 'countcart':countcart})


def deletecart(request, pk):
    cartitem = Cart.objects.get(pk=pk)
    cartitem.delete()
    return redirect('cart')



def updatecart(request):
    if request.method == "POST" and request.user.is_authenticated:
        prod_id = request.POST.get('product_id')
        prod_qty = request.POST.get('product_qty')
        
        if prod_id and prod_qty:
            try:
                cart = get_object_or_404(Cart, user=request.user, product_id=prod_id)
                
                cart.product_qty = int(prod_qty)
                cart.total_price = cart.product_qty * cart.product.Price
                cart.save()
                return JsonResponse({'status': 'updated successfully'})
                

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})





