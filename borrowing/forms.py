from django import forms
from .models import Borrow
from students.models import Student
from books.models import Book

class BorrowForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        empty_label="Select Student",
        widget=forms.Select(attrs={'class': 'form-control searchable'})
    )

    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        empty_label="Select Book",
        widget=forms.Select(attrs={'class': 'form-control searchable'})
    )

    class Meta:
        model = Borrow
        fields = ['student', 'book', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Student dropdown text: enrollment/roll + name
        self.fields['student'].label_from_instance = lambda obj: f"{obj.roll_number} - {obj.name}"

        # Book dropdown text: title + author
        self.fields['book'].label_from_instance = lambda obj: f"{obj.title} - {obj.author}"