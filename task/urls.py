from django.urls import path, re_path, include  # noqa
from . import views

urlpatterns = [

    re_path(r'^add_new_task/(?P<display_board>.*)$', views.add_new_task,
            name='add_new_task'),

    path('edit-task/<int:task_id>', views.edit_task,
         name='edit_task'),
    path('edit-task/<str>', views.edit_task,
         name='edit_task'),

    path('archive_task/<int:task_id>', views.archive_task,
         name='archive_task'),
    path('archive_task/', views.archive_task,
         name='archive_task'),

    path('delete_task/<int:task_id>', views.delete_task, name='delete_task')

]
