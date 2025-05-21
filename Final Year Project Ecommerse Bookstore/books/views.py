from django.shortcuts import get_object_or_404, render 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Book, Order
from django.urls import reverse_lazy
from django.db.models import Q # for search method
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from books.models import BookView,BookOrder
from books.models import Book  
#from .models import Book, Review
from django.shortcuts import redirect



from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


class BooksListView(ListView):
    model = Book
    template_name = 'list.html'


class BooksDetailView(DetailView):
    model = Book
    template_name = 'detail.html'
    
from .models import Book, Review
#from .forms import ReviewForm
from django.shortcuts import redirect

from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review



def books_detail(request, pk):
    print("book_detail view loaded with pk =", pk) 
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all().order_by('-created_at')
    

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                return redirect('books_detail', pk=pk)
        else:
            return redirect('login')
    else:
        form = ReviewForm()

    return render(request, 'detail.html', {
        'book': book,
        'form': form,
        'reviews': reviews
    })

class SearchResultsListView(ListView):
	model = Book
	template_name = 'search_results.html'

	def get_queryset(self): # new
		query = self.request.GET.get('q')
		return Book.objects.filter(
		Q(title__icontains=query) | Q(author__icontains=query)
		)

class BookCheckoutView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'checkout.html'
    login_url     = 'login'


def paymentComplete(request):
	body = json.loads(request.body)
	print('BODY:', body)
	product = Book.objects.get(id=body['productId'])
   
	Order.objects.create(
		product=product
	)
   
	return JsonResponse('Payment completed!', safe=False)

def process_upi_payment(request):
    if request.method == 'POST':
        upi_id = request.POST.get('upi_id')
        upi_app = request.POST.get('upi_app')
        
        # Here, you can log/store UPI info or validate in a real app
        print(f"Received UPI Payment from {upi_id} via {upi_app}")
        
        # Simulate a payment success page
        return HttpResponse(f"<h2>Thank you for your order. We'll start processing it right away.</h2><p>Thank you for your payment.</p>")
    
    return redirect('/')  # fallback if not POST

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt  # Optional if you're testing

@csrf_exempt  # Remove this line in production (for security)
def process_debit_payment(request):
    if request.method == 'POST':
        # Simulate debit card payment processing
        card_number = request.POST.get('card_number')
        expiry = request.POST.get('expiry')
        cvv = request.POST.get('cvv')

        # Add basic validation / dummy logic
        if card_number and expiry and cvv:
            # You could log this or simulate saving to DB
            print("Processing payment...")
            return redirect('complete')  # Redirect to success page
        else:
            return render(request, 'checkout.html', {'error': 'Missing card details'})

    return redirect('checkout')

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or redirect to homepage
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

import json
from django.http import JsonResponse



import json
from django.http import JsonResponse

def payment_complete_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("✅ Payment Data:", data)
            return JsonResponse({'message': 'Payment complete!'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'GET method not allowed. Please use POST with JSON data.'}, status=405)



from django.shortcuts import render

def complete(request):
    return render(request, 'complete.html')

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json

@csrf_exempt
def paymentComplete(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                print("Payment Data (JSON):", data)
                return JsonResponse({'message': 'Payment complete!'})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            # Handle non-JSON (form POST, e.g. Debit Card)
            print("Payment Data (Form):", request.POST)
            return HttpResponse("Payment completed successfully via form POST.")
    else:
        return JsonResponse({'error': 'GET method not allowed. Please use POST.'}, status=405)
    
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book  # Or your actual model
from django.http import HttpResponse

def add_to_cart(request, book_id):
    cart = request.session.get('cart', {})
    cart[book_id] = cart.get(book_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, book_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        if str(book_id) in cart:
            del cart[str(book_id)]
            request.session['cart'] = cart
    return redirect('cart')



def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for book_id, quantity in cart.items():
        book = get_object_or_404(Book, id=book_id)
        items.append({
            'book': book,
            'quantity': quantity,
            'subtotal': quantity * book.price
        })
        total += quantity * book.price
    return render(request, 'cart.html', {'items': items, 'total': total})

def checkout(request):
    return render(request, 'checkout.html')

def buy_now(request):
    # Clear the cart after successful checkout
    request.session['cart'] = {}
    return render(request, 'checkout.html')

def payment(request):
    return render(request, 'payment.html')



def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.user.is_authenticated:
        BookView.objects.create(user=request.user, book=book)
    book = get_object_or_404(Book, id=book_id)
    book.views += 1
    book.save()
    return render(request, 'detail.html', {'book': book})



def order_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))

        # Store order detail
        BookOrder.objects.create(user=request.user, book=book, quantity=quantity)

        # Increment real order count for analytics/export
        book.orders += quantity  # count orders based on quantity
        book.save()

        return redirect('order_success')

    return render(request, 'order_confirm.html', {'book': book})

from django.contrib.auth.decorators import login_required

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_id = review.book.id
    review.delete()
    return redirect('book_detail', pk=book_id)

from .models import Book, Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')  # Ensure user is logged in to comment
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = book.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.book = book
                comment.user = request.user
                comment.save()
                return redirect('book_detail', book_id=book_id)
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            comment.delete()
            return redirect('book_detail', book_id=book_id)
    else:
        form = CommentForm()

    return render(request, 'books/detail.html', {
        'book': book,
        'comments': comments,
        'form': form,
    })
