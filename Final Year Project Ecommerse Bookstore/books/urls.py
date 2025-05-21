
from django.urls import include, path
from .views import BooksListView, BooksDetailView, BookCheckoutView, book_detail, paymentComplete, SearchResultsListView
from . import views
from books import views



urlpatterns = [
    path('', BooksListView.as_view(), name = 'list'),
    path('<int:pk>/', BooksDetailView.as_view(), name = 'detail'),
    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name = 'checkout'),
    path('complete/', paymentComplete, name = 'complete'),
    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
    path('process_upi_payment/', views.process_upi_payment, name='process_upi_payment'),
    path('process_debit_payment/', views.process_debit_payment, name='process_debit_payment'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('payment-complete/', views.payment_complete_api, name='payment_complete_api'),
    path('complete/', views.complete, name='complete'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('buy_now/', views.buy_now, name='buy_now'),
    path('payment/', views.payment, name='payment'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    



    
    

   
    

]