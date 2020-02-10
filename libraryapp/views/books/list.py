import sqlite3
from django.shortcuts import render
from libraryapp.models import Book
from ..connection import Connection


def book_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                b.id,
                b.title,
                b.ISBN_number,
                b.author,
                b.year,
                b.librarian_id,
                b.location_id
            from libraryapp_book b
            """)

            all_books = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                book = Book()
                book.id = row['id']
                book.title = row['title']
                book.ISBN_number = row['ISBN_number']
                book.author = row['author']
                book.year = row['year']
                book.librarian_id = row['librarian_id']
                book.location_id = row['location_id']

                all_books.append(book)

        template = 'books/list.html' #holding the path and filename of the template created in templates/list.html
        context = {
            'all_books': all_books
        }

        return render(request, template, context)