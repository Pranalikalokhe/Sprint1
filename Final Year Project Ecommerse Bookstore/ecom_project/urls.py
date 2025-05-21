"""ecom_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from books import views
from books.views import BooksDetailView, book_detail, logout_view

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('', include("accounts.urls")), 
    path('accounts/', include("django.contrib.auth.urls")),   # working for login.html
    path('accounts/logout/', logout_view, name='logout'),
    path('logout/', logout_view, name='logout'),
    path('process_debit_payment/', views.process_debit_payment, name='process_debit_payment'),
    path('accounts/signup/', views.signup, name='signup'),
    path('complete/', views.complete, name='complete'),
    path('payment-complete/', views.payment_complete_api, name='payment_complete_api'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('payment/', views.payment, name='payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('', include('books.urls')), 
    
]    
    


   





