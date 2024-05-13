from django.contrib import admin
from .models import Task, Subtask


# Register your models here.
admin.site.register(Subtask)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('on_board', 'title', 'description', 'priority',
                    'show_status', 'completed',
                    'archived', 'show_labels', 'completed_on')

    def on_board(self, obj):
        board = Task.objects.filter(id=obj.id).first().column.board
        return board.title
    on_board.short_description = 'On Board'

    def show_labels(self, obj):
        labels = Task.objects.filter(id=obj.id).first().label.all()
        return [label.title for label in labels]
    show_labels.short_description = 'Labels'

    def show_status(self, obj):
        status = Task.objects.filter(id=obj.id).first().column.title
        return status
    show_status.short_description = 'Status (Column)'
