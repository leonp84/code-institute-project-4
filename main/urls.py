from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:display_board>', views.index, name='show_board'),
    path('create_new_board/', views.create_new_board,
         name='create_new_board'),
    path('add-task/', views.add_new_task,
         name='add_new_task')
]
