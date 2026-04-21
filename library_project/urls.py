from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('students/', include('students.urls')),
    path('borrowing/', include('borrowing.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]