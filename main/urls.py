from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_edit_board/', views.create_edit_board, 
         name='create_edit_board')
]
