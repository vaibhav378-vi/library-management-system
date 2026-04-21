from django.urls import path
from . import views

urlpatterns = [
    path('', views.borrow_list, name='borrow_list'),
    path('add/', views.borrow_add, name='borrow_add'),
    path('return/<int:id>/', views.borrow_return, name='borrow_return'),
]