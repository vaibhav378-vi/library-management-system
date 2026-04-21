from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student
from .forms import StudentForm
from borrowing.models import Borrow

def is_admin(user):
    return user.is_staff or user.is_superuser

def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(name__icontains=query) | Student.objects.filter(roll_number__icontains=query) | Student.objects.filter(department__icontains=query)
    else:
        students = Student.objects.all()

    return render(request, 'students/student_list.html', {'students': students})

@user_passes_test(is_admin)
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {'form': form})

@user_passes_test(is_admin)
def student_edit(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {'form': form})

@user_passes_test(is_admin)
def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')

    return render(request, 'students/student_confirm_delete.html', {'student': student})

@login_required
def my_books(request):
    try:
        student = Student.objects.get(user=request.user)
        borrows = Borrow.objects.filter(student=student).order_by('-id')
        return render(request, 'students/my_books.html', {'borrows': borrows})
    except Student.DoesNotExist:
        messages.error(request, 'Your account is not linked to any student profile.')
        return redirect('home')