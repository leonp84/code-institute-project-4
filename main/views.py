from django.shortcuts import render, HttpResponse  # noqa
from django.contrib.auth.decorators import login_required
from .forms import CreateBoardForm, CreateNewTaskForm
from .models import Board, Column, Label


# Create your views here.
@login_required
def index(request, display_board=None):
    all_boards = Board.objects.all()

    if display_board is not None:
        current_board = Board.objects.all().filter(pk=display_board).first()
        print('Current Board = ' + str(current_board))
    else:
        current_board = Board.objects.all().first

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


def add_new_task(request):
    all_boards = Board.objects.all()
    current_board = Board.objects.all().first

    if request.method == 'POST':
        queryset = CreateNewTaskForm(data=request.POST)
        new_task = queryset.save(commit=False)
        task_to_column = request.POST.get('status')
        new_task.column = Column.objects.filter(id=task_to_column).first()
        new_task.save()

    return render(
        request,
        'main/index.html',
        {'all_boards': all_boards,
         'board': current_board}
        )
