from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_new_board/', views.create_new_board,
         name='create_new_board')
]
