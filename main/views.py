from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CreateBoardForm, CreateNewTaskForm
from .models import Board, Column, Label, Subtask, Task


# Create your views here.
@login_required
def index(request, display_board=None):
    all_boards = Board.objects.all()

    if display_board is not None:
        current_board = Board.objects.all().filter(pk=display_board).first()
    else:
        current_board = Board.objects.all().first()

    return render(
        request,
        'main/index.html',
        {'all_boards': all_boards,
         'board': current_board}
        )


def create_new_board(request):

    current_board = Board.objects.all().first()
    all_boards = Board.objects.all()

    if request.method == 'POST':

        user_input = CreateBoardForm(data=request.POST)
        if user_input.is_valid():
            new_board = user_input.save(commit=False)
            new_board.author = request.user
            new_board.save()

        # Add new Column Instance(s)
        add_cols = request.POST.getlist('column_title')
        for i in range(1, len(add_cols)+1):
            new_column = Column(
                title=add_cols[i-1],
                colour=request.POST.get(f'column_colour-{i}'),
                board=new_board
            )
            new_column.save()

        # Add new Label Instance(s)
        add_labels = request.POST.getlist('label_title')
        for i in range(1, len(add_labels)+1):
            new_label = Label(
                title=add_labels[i-1],
                colour=request.POST.get(f'label_colour-{i}'),
                board=new_board
            )
            new_label.save()

        # Return to index.html with new Board instance
        current_board = Board.objects.all().first()

        return render(
            request,
            'main/index.html',
            {'all_boards': all_boards,
             'board': current_board}
            )

    return render(
        request,
        'main/create_new_board.html',
        {'all_boards': all_boards,
            'board': current_board}
        )


def add_new_task(request, display_board):
    all_boards = Board.objects.all()
    current_board = Board.objects.all().filter(pk=display_board).first()

    if request.method == 'POST':
        queryset = CreateNewTaskForm(data=request.POST)
        if queryset.is_valid():
            new_task = queryset.save(commit=False)
        else:
            print(queryset.errors)

        # Add Task Column
        task_to_column = request.POST.get('status')
        new_task.column = Column.objects.filter(id=task_to_column).first()
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

    return render(
        request,
        'main/index.html',
        {'all_boards': all_boards,
         'board': current_board}
        )


def edit_task(request, task_id):

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
    else:
        task_to_edit.completed = False

    task_to_edit.save()

    # Update Subtasks
    queryset = request.POST.getlist('subtasks')
    for subtask in task_to_edit.subtask_to_task.all():
        if str(subtask.id) in queryset:
            subtask.status = True
        else:
            subtask.status = False
        subtask.save()

    # Update Labels
    task_to_edit.label.clear()
    queryset = request.POST.getlist('new-label')
    for id in queryset:
        new_label = Label.objects.filter(id=id).first()
        task_to_edit.label.add(new_label)

    all_boards = Board.objects.all()

    return render(
        request,
        'main/index.html',
        {'all_boards': all_boards,
         'board': current_board}
        )


def edit_board(request, board_id):

    all_boards = Board.objects.all()
    current_board = Board.objects.filter(id=board_id).first()

    if request.method == 'POST':
        # Update Board Title & Description
        current_board.title = request.POST.get('title')
        current_board.description = request.POST.get('description')
        current_board.save()

        # Update Column Titles & Colours
        new_column_names = request.POST.getlist('column_title')
        update_columns = request.POST.getlist('column-id')

        for i in range(len(new_column_names)):
            # Update Existing Column (Current column.id = present)
            if i < len(update_columns):

                current_column = Column.objects.filter(
                    id=update_columns[i]).first()
                current_column.title = new_column_names[i]
                current_column.colour = request.POST.get(
                    f'column_colour-{i+1}')
                current_column.save()
            # Create New Column (Since no current column.id present)
            else:
                new_column = Column(
                    title=new_column_names[i],
                    colour=request.POST.get(f'column_colour-{i+1}'),
                    board=current_board
                )
                new_column.save()

        # Update Label Titles & Colours
        new_label_names = request.POST.getlist('label_title')
        update_labels = request.POST.getlist('label-id')

        for i in range(len(new_label_names)):
            # Update Existing label (Current label.id = present)
            if i < len(update_labels):

                current_label = Label.objects.filter(
                    id=update_labels[i]).first()
                current_label.title = new_label_names[i]
                current_label.colour = request.POST.get(
                    f'label_colour-{i+1}')
                current_label.save()
            # Create New label (Since no current label.id present)
            else:
                new_label = Label(
                    title=new_label_names[i],
                    colour=request.POST.get(f'label_colour-{i+1}'),
                    board=current_board
                )
                new_label.save()

        all_boards = Board.objects.all()

        return render(
            request,
            'main/edit_board.html',
            {'all_boards': all_boards,
             'board': current_board}
            )

    return render(
        request,
        'main/edit_board.html',
        {'all_boards': all_boards,
         'board': current_board}
        )


def archive_task(request, task_id):

    print('Task to archive logic')

    task_to_archive = Task.objects.filter(id=task_id).first()
    task_to_archive.archived = True
    task_to_archive.save()

    current_board = Board.objects.filter(
        id=task_to_archive.column.board.id).first()
    all_boards = Board.objects.all()

    return render(
        request,
        'main/index.html',
        {'all_boards': all_boards,
         'board': current_board}
        )


def delete_task(request, task_id):

    task_to_delete = Task.objects.filter(id=task_id).first()

    current_board = Board.objects.filter(
        id=task_to_delete.column.board.id).first()

    task_to_delete.delete()

    all_boards = Board.objects.all()

    return render(
        request,
        'main/index.html',
        {'all_boards': all_boards,
         'board': current_board}
        )
