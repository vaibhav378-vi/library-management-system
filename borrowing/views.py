from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from .models import Borrow
from .forms import BorrowForm

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def borrow_list(request):
    borrows = Borrow.objects.all().order_by('-id')
    return render(request, 'borrowing/borrow_list.html', {'borrows': borrows})

@user_passes_test(is_admin)
def borrow_add(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book issued successfully.')
            return redirect('borrow_list')
    else:
        form = BorrowForm()

    return render(request, 'borrowing/borrow_form.html', {'form': form})

@user_passes_test(is_admin)
def borrow_return(request, id):
    borrow = get_object_or_404(Borrow, id=id)

    if not borrow.is_returned:
        borrow.is_returned = True
        borrow.return_date = timezone.now().date()
        borrow.save()
        messages.success(request, f'Book returned successfully. Fine: ₹{borrow.fine_amount}')

    return redirect('borrow_list')