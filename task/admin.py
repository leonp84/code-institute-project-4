from django.contrib import admin
from .models import Task, Subtask

admin.site.register(Subtask)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    '''
    Register TaskAdmin model to display detailed Task information for site
    admin users. This model displays tasks with their status, priority and
    whether or not they are in the board archive.
    '''
    list_display = ('board_name', 'title', 'description', 'priority',
                    'column', 'completed', 'archived',
                    'show_labels', 'completed_on')
    list_filter = ('completed',)

    def show_labels(self, obj):
        labels = Task.objects.filter(id=obj.id).first().label.all()
        return [label.title for label in labels]
    show_labels.short_description = 'Labels'
