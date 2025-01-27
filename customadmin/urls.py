from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard', views.admin_dashboard, name='dashboard'),
    path('adlogout', views.admin_logout, name='adlogout'),
    path('userlist', views.user_list, name='userlist'),
    path('delete/<pk>', views.delete, name='delete'),
    path('addproduct', views.add_product, name='addproduct'),
    path('deleteprod/<pk>', views.deleteprod, name='deleteprod'),
    path('deletecat/<pk>', views.deletecat, name='deletecat'),
    path('editprod/<pk>', views.editproduct, name='editprod'),
    path('viewproduct', views.view_product, name='viewproduct'),
    path('categories', views.categories, name='categories'),
    path('adcoupon', views.Couponcodes, name='adcoupon'),
    path('deletecoupon/<pk>', views.deletecoupon, name='deletecoupon'),
    path('editcoupon/<int:pk>', views.editcoupon, name='editcoupon'),
    path('orders', views.order_management, name='orders')
]