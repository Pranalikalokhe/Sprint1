# import csv
# from django.core.management.base import BaseCommand
# from books.models import BookView, BookOrder  # change 'books' if your app name is different

# class Command(BaseCommand):
#     help = 'Export book view and order data to CSV'

#     def handle(self, *args, **kwargs):
#         with open('book_data.csv', 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(['book_id', 'views', 'orders'])

#             book_ids = set(BookView.objects.values_list('book_id', flat=True)) | set(BookOrder.objects.values_list('book_id', flat=True))
            
#             for book_id in book_ids:
#                 views = BookView.objects.filter(book_id=book_id).count()
#                 orders = BookOrder.objects.filter(book_id=book_id).count()
#                 writer.writerow([book_id, views, orders])

#         self.stdout.write(self.style.SUCCESS('Data exported successfully to book_data.csv'))
# import os
# import csv
# from django.core.management.base import BaseCommand
# from books.models import Book  # use your actual model name

# class Command(BaseCommand):
#     help = 'Export book data to CSV'

#     def handle(self, *args, **options):
#         os.makedirs('data', exist_ok=True)  # ✅ Create 'data' folder if it doesn't exist

#         file_path = 'data/book_data.csv'
#         with open(file_path, 'w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(['ID', 'Title', 'Author', 'Price','views', 'orders'])  # adjust fields as needed

#             for book in Book.objects.all():
#                 writer.writerow([book.id, book.title, book.author, book.price, book.views, book.orders])

#         self.stdout.write(self.style.SUCCESS(f'Data exported successfully to {file_path}'))
        
        
# export_data.py

import csv
from django.core.management.base import BaseCommand
from books.models import Book

class Command(BaseCommand):
    help = 'Export book data to CSV'

    def handle(self, *args, **kwargs):
        with open('data/book_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Title', 'Author', 'Price','views', 'orders'])  # include orders
            for book in Book.objects.all():
                writer.writerow([book.id, book.title, book.author, book.price, book.views, book.orders])
        self.stdout.write(self.style.SUCCESS('Data exported successfully to data/book_data.csv'))
