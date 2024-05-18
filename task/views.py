from django.shortcuts import HttpResponseRedirect, reverse
from datetime import datetime
from .models import Task, Subtask
from main.models import Board, Column, Label
from .forms import CreateNewTaskForm


def add_new_task(request, display_board=None):
    '''
    Creates a new instance of :model:`task.Task` and links it
    to a specific instance of :model:`main.Column`. Each instance
    contains one or more links to :model:`task.Subtask` and/or
    :model:`main.Label`. This instance is then returned to the main
    landing page to be displayed with other tasks.
    **Context**
    ```display_board```
        The primary key of the current :model:`main.Board`
        to be displayed on the landing page.
    **Template**
        :template:`main/index.html`
    '''
    if request.method == 'POST':
        queryset = CreateNewTaskForm(data=request.POST)
        if queryset.is_valid():
            new_task = queryset.save(commit=False)
        else:
            print(queryset.errors)

        # Add Task Column
        task_to_column = request.POST.get('status')

        new_task.column = Column.objects.filter(id=task_to_column).first()
        new_task.completed = False
        new_task.save()

        # Add Task Subtasks
        subtasks = request.POST.getlist('subtasks')
        for title in subtasks:
            if title:
                subtask = Subtask(
                    title=title,
                    task=new_task
                )
                subtask.save()

        # Add Task Labels
        label_ids = request.POST.getlist('label')
        for id in label_ids:
            new_label = Label.objects.filter(id=id).first()
            new_task.label.add(new_label)

    return HttpResponseRedirect(reverse('show_board', args=[display_board]))


def edit_task(request, task_id=None):
    '''
    Allows editing of one instance of :model:`task.Task` and
    saves this instance to the database with newly updated information
    including any new connections to :model:`main.Column`,
    :model:`task.Subtask` and :model:`main.Label`.
    This edited instance is then returned to the main
    landing page to be displayed with other tasks.
    **Context**
    ```current_board.id```
        The primary key of the current :model:`main.Board`
        to be displayed on the landing page.
    **Template**
        :template:`main/index.html`
    '''
    task_to_edit = Task.objects.filter(id=task_id).first()
    current_board = Board.objects.filter(
        id=task_to_edit.column.board.id).first()

    # Update Priority
    task_to_edit.priority = request.POST.get('priority')

    # Update Status (Column)
    task_to_column = request.POST.get('status')
    task_to_edit.column = Column.objects.filter(id=task_to_column).first()

    # Update Completion = True / False
    if task_to_edit.column.id == current_board.column_to_board.last().id:
        task_to_edit.completed = True
        task_to_edit.completed_on = datetime.now()
    else:
        task_to_edit.completed = False

    task_to_edit.save()

    # Update Subtasks
    queryset = request.POST.getlist('subtasks')
    for subtask in task_to_edit.subtask_to_task.all():
        if str(subtask.id) in queryset:
            subtask.status = True
            subtask.completed_on = datetime.now()
        else:
            subtask.status = False
        subtask.save()

    # Update Labels
    task_to_edit.label.clear()
    queryset = request.POST.getlist('new-label')
    for id in queryset:
        new_label = Label.objects.filter(id=id).first()
        task_to_edit.label.add(new_label)

    return HttpResponseRedirect(reverse('show_board', args=[current_board.id]))


def archive_task(request, task_id=None):
    '''
    Allows update of the task.archived field of one instance
    of :model:`task.Task` and saves the instance to the
    database. This edited instance is then returned to the main
    landing page to be displayed with other tasks.
    **Context**
    ```current_board.id```
        The primary key of the current :model:`main.Board`
        to be displayed on the landing page.
    **Template**
        :template:`main/index.html`
    '''
    task_to_archive = Task.objects.filter(id=task_id).first()
    task_to_archive.archived = True
    task_to_archive.save()

    current_board = Board.objects.filter(
        id=task_to_archive.column.board.id).first()
    current_board.has_archived_tasks = True
    current_board.save()

    return HttpResponseRedirect(reverse('show_board', args=[current_board.id]))


def delete_task(request, task_id=None):
    '''
    Allows deletion of one instance of :model:`task.Task`.
    After deletion, the view redirects to the main
    landing page to be displayed without the deleted task.
    **Context**
    ```current_board.id```
        The primary key of the current :model:`main.Board`
        to be displayed on the landing page.
    **Template**
        :template:`main/index.html`
    '''
    task_to_delete = Task.objects.filter(id=task_id).first()
    current_board = Board.objects.filter(
        id=task_to_delete.column.board.id).first()
    task_to_delete.delete()

    return HttpResponseRedirect(reverse('show_board', args=[current_board.id]))
