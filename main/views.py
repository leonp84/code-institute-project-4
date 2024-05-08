from django.shortcuts import render, HttpResponse  # noqa
from django.contrib.auth.decorators import login_required
from .forms import CreateBoardForm
from .models import Board


# Create your views here.
@login_required
def index(request):
    boards = Board.objects.all()

    return render(
        request,
        'main/index.html',
        {'boards': boards}
        )


def create_edit_board(request):
    create_board_form = CreateBoardForm()

    if request.method == 'POST':
        user_input = CreateBoardForm(data=request.POST)
        if user_input.is_valid:
            new_board = user_input.save(commit=False)
            new_board.author = request.user
            new_board.save()
        else:
            print(user_input.errors)

        boards = Board.objects.all()

        return render(
            request,
            'main/index.html',
            {'boards': boards}
            )

    return render(
        request,
        'main/create_edit_board.html',
        {'create_board_form': create_board_form}
    )
