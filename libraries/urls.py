from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.add_library, name='add_library'),
    path('', views.library_list, name='library_list'),
    path('<int:pk>/', views.library_detail, name='library_detail'),

    path('<int:library_pk>/add_book/', views.add_book_to_library, name='add_book_to_library'),





]
