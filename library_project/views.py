from django.shortcuts import render
from books.models import Book
from students.models import Student
from borrowing.models import Borrow

def home(request):
    total_books = Book.objects.count()
    total_students = Student.objects.count()
    issued_books = Borrow.objects.filter(is_returned=False).count()
    returned_books = Borrow.objects.filter(is_returned=True).count()

    context = {
        'total_books': total_books,
        'total_students': total_students,
        'issued_books': issued_books,
        'returned_books': returned_books,
    }
    return render(request, 'home.html', context)