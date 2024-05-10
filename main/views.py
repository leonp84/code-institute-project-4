from django.shortcuts import render, HttpResponse  # noqa
from django.contrib.auth.decorators import login_required
from .forms import CreateBoardForm
from .models import Board, Column, Label


# Create your views here.
@login_required
def index(request):
    board = Board.objects.all().first()
    for item in board.board_to_column.all():
        print(item.title)
    return render(
        request,
        'main/index.html',
        {'board': board}
        )


def create_new_board(request):

    if request.method == 'POST':

        user_input = CreateBoardForm(data=request.POST)
        if user_input.is_valid:
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
        board = Board.objects.all().first()

        return render(
            request,
            'main/index.html',
            {'board': board}
            )

    return render(
        request,
        'main/create_new_board.html',
    )
