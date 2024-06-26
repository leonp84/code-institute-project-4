from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html, urlencode
from .models import Board, Column, Label
from task.models import Task

admin.site.register(Column)
admin.site.register(Label)

admin.site.site_header = "TaskFlow - Admin Panel"
admin.site.site_title = "Admin Panel"
admin.site.index_title = 'TaskFlow Dashboard'


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    '''
    Register BoardAdmin model to display detailed board information for site
    admin users on the Admin page. This model displays open and closed tasks
    per board with a link that takes admin users to all open tasks in the
    current board.
    '''
    list_display = ('title', 'description', 'author',
                    'show_columns', 'show_labels',
                    'open_tasks', 'archived_tasks')

    def show_columns(self, obj):
        nr_columns = Board.objects.filter(id=obj.id).first(
            ).column_to_board.all().count()
        return nr_columns
    show_columns.short_description = '#Columns'

    def show_labels(self, obj):
        nr_labels = Board.objects.filter(id=obj.id).first(
            ).label_to_board.all().count()
        return nr_labels
    show_labels.short_description = '#Labels'

    def open_tasks(self, obj):
        total_tasks = 0
        open_tasks = 0
        cols = Board.objects.filter(id=obj.id).first().column_to_board.all()
        for column in cols:
            total_tasks += column.task_to_column.all().count()
            open_tasks += column.task_to_column.filter(completed=False).count()

        url = (
            reverse("admin:task_task_changelist")
            + "?"
            + urlencode({"completed": False})
        )
        return format_html(
            '<a href="{}">{}</a>/{}', url, open_tasks, total_tasks)
    open_tasks.short_description = 'Open/Total Tasks'

    def archived_tasks(self, obj):
        archived_tasks = Task.objects.filter(archived=True).count()
        return archived_tasks
    archived_tasks.short_description = 'Archived Tasks'
