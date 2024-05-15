from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import CreateBoardForm
from .models import Board, Column, Label
from task.models import Task
from django.http import JsonResponse
import json


# Create your views here.
@login_required
def index(request, display_board=None):

    if request.user.board_to_user.all().count() == 0:
        create_initial_board(request)

    all_boards = Board.objects.all()
    if display_board is not None:
        current_board = Board.objects.all().filter(pk=display_board).first()
    else:
        current_board = Board.objects.all().first()

    return render(
        request,
        'main/index.html',
        {'all_boards': all_boards,
         'board': current_board,
         'home': True}
        )


def create_new_board(request):
    all_boards = Board.objects.all()
    current_board = Board.objects.all().first()

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

        return HttpResponseRedirect(reverse('show_board', args=[new_board.id]))

    return render(
        request,
        'main/create_new_board.html',
        {'all_boards': all_boards,
            'board': current_board}
        )


def edit_board(request, board_id=None):

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

        return HttpResponseRedirect(reverse('show_board', args=[board_id]))

    return render(
        request,
        'main/edit_board.html',
        {'all_boards': all_boards,
         'board': current_board}
        )


def search(request, board_id):

    all_boards = Board.objects.all()
    current_board = Board.objects.filter(id=board_id).first()

    current_board_tasks = Task.objects.filter(
        column__in=current_board.column_to_board.all())

    if request.method == 'POST':
        user_search = request.POST.get('user_search')
        search_results = current_board_tasks.filter(
            title__icontains=user_search) | current_board_tasks.filter(
            description__icontains=user_search)

        count = len(search_results)
        print(search_results)

    return render(
        request,
        'main/search_results.html',
        {'all_boards': all_boards,
         'board': current_board,
         'search_results': search_results,
         'user_search': user_search,
         'count': count,
         'home': True}
        )


def create_initial_board(request):

    first_board = Board(
        title='Kanban',
        description='Kanban (Japanese: 看板, meaning signboard or billboard) is '
                    'a lean method to manage and improve work across human '
                    'systems. This approach aims to manage work by balancing '
                    'demands with available capacity, and by improving the '
                    'handling of system-level bottlenecks. - Wikipedia',

        author=request.user
    )
    first_board.save()

    first_column = Column(
        title='Todo',
        colour='blue',
        board=first_board
    )
    first_column.save()

    second_column = Column(
        title='Doing',
        colour='yellow',
        board=first_board
    )
    second_column.save()

    third_column = Column(
        title='Done',
        colour='green',
        board=first_board
    )
    third_column.save()

    new_label = Label(
        title='task',
        colour='primary',
        board=first_board
    )
    new_label.save()

    new_task = Task(
        title='Click to edit or delete this sample task',
        description='You can edit this board by adding new columns'
                    ' and/or labels. Click on "Edit Current Board" '
                    ' above.',
        priority='green',
        column=first_column
    )
    new_task.save()
    new_task.label.add(new_label)

    return HttpResponseRedirect(reverse('show_board', args=[first_board.id]))


def update_status(request):
    if request.method == 'POST':
        data = json.load(request)
        new_column = data['newColumnName']
        tasks_in_column = data['tasksInColumn']

    for i in range(len(tasks_in_column)):
        task_to_update = Task.objects.filter(title=tasks_in_column[i]).first()
        task_to_update.column = Column.objects.filter(title=new_column).first()
        task_to_update.column_position = i
        task_to_update.save()

    return JsonResponse({'message': 'Model Updated'})
