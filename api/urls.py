from django.urls import path
from admin_dashboard import views

urlpatterns = [
    path('banners', views.banners),
    path('banners/<int:pk>', views.bannerMethods),
    path('category', views.category),
    path('category/<int:pk>', views.categoryMethods),
    path('products', views.products),
    path('products/<int:pk>', views.productMethods),
    path('testimonials', views.testimonials),
    path('testimonials/<int:pk>', views.testimonialMethods)

]