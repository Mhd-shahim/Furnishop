from django.urls import path
from home import views,cart

urlpatterns = [
    path('',views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('login/',views.login, name='login'),
    path('logout/',views.userlogout, name='userlogout'),
    path('register/', views.register, name='register'),
    path('singleproduct/<pk>', views.singleproduct, name='singleproduct'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('viewwishlist/', views.viewwishlist, name="viewwishlist"),
    path('deletewishlist/<pk>', views.deletewishlist, name='deletewishlist'),
    path('movetocart/', views.movetocart, name='movetocart'),
    path('deleteprofile/', views.deleteprofile, name='deleteprofile'),
    path('checkout/', views.checkout, name='checkout'),
    path('coupon/', views.coupen, name="coupen"),
    path('placeorder/', views.place_order, name="placeorder"),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('billing/', views.billing, name='billing'),
    path('newaddress/', views.newaddres, name="nwwaddress"),
    path('about/', views.about, name="about"),
    path('service/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    #otp
    path('otp/', views.home, name='home'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    #cart.py
    path('add-to-cart', cart.addtocart, name="addtocart"),
    path('cart/', cart.viewcart, name='cart'),
    path('dltcart/<pk>',cart.deletecart, name='deletecartitem' ),
    path('update-cart', cart.updatecart, name='updatecart'),
    
]

