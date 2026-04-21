from django.db import models
from students.models import Student
from books.models import Book
from django.utils import timezone

class Borrow(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    fine_amount = models.PositiveIntegerField(default=0)

    def calculate_fine(self):
        fine_per_day = 5

        if self.is_returned and self.return_date and self.return_date > self.due_date:
            late_days = (self.return_date - self.due_date).days
            return late_days * fine_per_day

        elif not self.is_returned and timezone.now().date() > self.due_date:
            late_days = (timezone.now().date() - self.due_date).days
            return late_days * fine_per_day

        return 0

    def save(self, *args, **kwargs):
        self.fine_amount = self.calculate_fine()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.book.title}"