from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404  # noqa
import json
from .forms import CreateBoardForm
from .models import Board, Column, Label
from task.models import Task


@login_required
def index(request, display_board=None, message=None):
    '''
    Populates the main landing page with the currently selected instance
    of :model:`main.Board` and its accompanying information.
    **Context**
    ```all_boards```
        Queryset containing all current instances of :model:`main.Board`
        connected to the current user account.
    ```board```
        The primary key of the current instance of :model:`main.Board`.
    ```home```
        A boolean variable instructing the template to display navbar
        links relevant to the home page.
    ```home```
        A string variable that instructs the landing page template to
        display messages whenever tasks have been added or updated.
    **Template**
        template:`main/index.html`
    '''
    if request.user.board_to_user.all().count() == 0:
        create_initial_board(request)

    # Using Django `.only()` to minimize database queries.
    all_boards = Board.objects.only('title', 'id').filter(author=request.user)
    if display_board is not None:
        # Using Django `prefetch_related` to minimize database queries.
        current_board = Board.objects.prefetch_related(
            'column_to_board',
            'column_to_board__task_to_column',
            'column_to_board__task_to_column__label',
            'column_to_board__task_to_column__subtask_to_task',
            'label_to_board'
        ).filter(id=display_board).first()
    else:
        current_board = Board.objects.filter(author=request.user).first()

    return render(
        request,
        'main/index.html',
        {'all_boards': all_boards,
         'board': current_board,
         'home': True,
         'message': message}
        )


@login_required
def create_new_board(request):
    '''
    Allows creation of one new instance of `main.Board`. Each instance
    is connected to its respective Columns - :model:`main.Column` and
    Labels - :model:`main.Label`. This newly created instance is then
    returned to the main landing page to be displayed.
    **Context**
    ```new_board.id```
        The primary key of the newly created :model:`main.Board`
        to be displayed on the landing page.
    ```all_boards```
        Queryset containing all current instances of :model:`main.Board`
        connected to the current user account.
    ```board```
        The primary key of the current instance of :model:`main.Board`
    **Template**
        GET :template:`create_new_board.html`
        POST :template:`main/index.html`
    '''
    all_boards = Board.objects.filter(author=request.user)
    current_board = Board.objects.filter(author=request.user).first()

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


@login_required
def edit_board(request, board_id=None):
    '''
    Allows editing of one existing instance of `main.Board`. Each instance
    is connected to its respective Columns - :model:`main.Column` and
    Labels - :model:`main.Label`. This newly edited instance is then
    returned to the main landing page to be displayed.
    **Context**
    ```board_id```
        The primary key of the newly edited :model:`main.Board`
        to be displayed on the landing page.
    ```all_boards```
        Queryset containing all current instances of :model:`main.Board`
        connected to the current user account.
    ```board```
        The primary key of the current instance of :model:`main.Board`
    **Template**
        GET :template:`main/edit_board.html`
        POST :template:`main/index.html`
    '''
    all_boards = Board.objects.filter(author=request.user)
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

        return HttpResponseRedirect(reverse(
            'show_board', args=[board_id, 'board_updated']))

    return render(
        request,
        'main/edit_board.html',
        {'all_boards': all_boards,
         'board': current_board}
        )


@login_required
def search(request, board_id):
    '''
    Allows a user to search through all instances of :model:`task.Task`
    on the current instance of :modal:`main.Board`. The view returns
    a queryset of search results to be displayed on a search results page.
    Task name and description fields are searched.
    **Context**
    ```all_boards```
        Queryset containing all current instances of :model:`main.Board`
        connected to the current user account.
    ```board```
        The primary key of the current instance of :model:`main.Board`.
    ```search_results```
        A queryset of found instances of :model:`task.Task`.
    ```user_search```
        A string variable containing the phrase searched by the user.
    ```count```
        An integer of the number of items found.
    ```home```
        A boolean variable confirming to the template to display navbar
        links relevant to the home page.
    **Template**
        GET :template:`main/edit_board.html`
        POST :template:`main/index.html`
    '''
    all_boards = Board.objects.filter(author=request.user)
    current_board = Board.objects.filter(id=board_id).first()

    current_board_tasks = Task.objects.filter(
        column__in=current_board.column_to_board.all())

    if request.method == 'POST':
        user_search = request.POST.get('user_search')
        search_results = current_board_tasks.filter(
            title__icontains=user_search) | current_board_tasks.filter(
            description__icontains=user_search)

        count = len(search_results)

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


@login_required
def create_initial_board(request):
    '''
    Relevant for newly created instances of :model:`auth.User`.
    Newly registered users do not start with empty Boards, instead, this
    view generates initial models for the landing page. It creates the 
    following instances:
    :model:`main.Board` x 1
    :model:`main.Column` x 3
    :model:`main.Label` x 1
    :model:`task.Task` x 1
    These instances are then returned to the main landing page to be
    displayed there.
    **Context**
    ```first_board.id```
        The primary key of the newly created instance of :model:`main.Board`
    **Template**
        :template:`main/index.html`
    '''
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


@login_required
def update_status(request):
    '''
    Updates instances of :model:`task.Task` through asyncronous Javascript
    whenever tasks are moved around through drag-and-drop. The view
    returns a Jsonresponse and does not cause any page reload.
    **Context**
    ```message```
        Internal Reply to Jquery (see `static/assets/js/index.js:67)
    '''
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
