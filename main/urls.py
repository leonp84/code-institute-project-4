from django.urls import path, re_path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('<int:display_board>', views.index, name='show_board'),

    path('create_new_board/', views.create_new_board,
         name='create_new_board'),

    re_path(r'^edit-board/(?P<board_id>.*)$', views.edit_board,
            name='edit_board'),

    re_path(r'^search/(?P<board_id>.*)$', views.search,
            name='search'),

    path('update_status/', views.update_status, name='update_status'),

]
