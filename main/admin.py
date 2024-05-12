from django.utils.html import format_html
from django.contrib import admin
from .models import Board, Column, Label, Task, Subtask

admin.site.register(Column)
admin.site.register(Label)
admin.site.register(Task)
admin.site.register(Subtask)

admin.site.site_header = "FlowTask - Admin Panel"
admin.site.site_title = "Admin Panel"
admin.site.index_title = 'FlowTask Dashboard'


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author',
                    'show_columns', 'open_tasks', 'archived_tasks')

    def show_columns(self, obj):
        nr_columns = Board.objects.filter(id=obj.id).first(
            ).column_to_board.all().count()
        return nr_columns
    show_columns.short_description = '#Columns'

    def open_tasks(self, obj):
        total_tasks = 0
        open_tasks = 0
        cols = Board.objects.filter(id=obj.id).first().column_to_board.all()
        for column in cols:
            total_tasks += column.task_to_column.all().count()
            open_tasks += column.task_to_column.filter(completed=True).count()

        return format_html("<b>{}</b>/{}", open_tasks, total_tasks)
    open_tasks.short_description = 'Open/Total Tasks'

    def archived_tasks(self, obj):
        archived_tasks = Task.objects.filter(archived=True).count()
        return archived_tasks
    archived_tasks.short_description = 'Archived Tasks'
