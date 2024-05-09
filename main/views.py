from django.shortcuts import render, HttpResponse  # noqa
from django.contrib.auth.decorators import login_required
from .forms import CreateBoardForm
from .models import Board, Column


# Create your views here.
@login_required
def index(request):
    boards = Board.objects.all()
    print('##########')
    # Xx.board_to_column.all().count())

    return render(
        request,
        'main/index.html',
        {'boards': boards}
        )


def create_edit_board(request):

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

        boards = Board.objects.all()

        return render(
            request,
            'main/index.html',
            {'boards': boards}
            )

    return render(
        request,
        'main/create_edit_board.html',
    )
