from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from todolist.models import Board, Task, Friend
from django.contrib.auth.decorators import login_required
from .forms import NewBoard, NewTask
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


@login_required
def add_board(request):
    if request.method == 'POST':
        if 'board' in str(request.POST):
            board_form = NewBoard(request.POST, prefix='board')
            if board_form.is_valid():
                user = request.user
                board = Board(name=board_form.cleaned_data['board_name'], username=user)
                board.save()
                return HttpResponseRedirect(reverse('todo'))
    return HttpResponseNotFound


@login_required
def add_task(request, pk):
    if request.method == 'POST':
        if 'task' in str(request.POST):
            task_form = NewTask(request.POST, prefix='task')
            if task_form.is_valid():
                board_obj = get_object_or_404(Board, pk=pk)
                task = Task(name=task_form.cleaned_data['task_name'], status=False, board=board_obj)
                task.save()
                return HttpResponseRedirect(reverse('todo'))
    return HttpResponseNotFound


@login_required
def check_task(request, pk):
    if request.method == 'POST':
        task_instance = get_object_or_404(Task, pk=pk)
        task_instance.status = False if task_instance.status else True
        task_instance.save()
        return HttpResponseRedirect(reverse('todo'))
    return HttpResponseNotFound()


@login_required
def delete_task(request, pk):
    if request.method == 'POST':
        task_instance = get_object_or_404(Task, pk=pk)
        task_instance.delete()
        return HttpResponseRedirect(reverse('todo'))
    return HttpResponseNotFound()


@login_required
def delete_board(request, pk):
    if request.method == 'POST':
        board_instance = get_object_or_404(Board, pk=pk)
        board_instance.delete()
        return HttpResponseRedirect(reverse('todo'))
    return HttpResponseNotFound()


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('todo')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='/accounts/login/')
def todo(request):
    todo_dict = {}
    index_position = 0
    username = request.user.id
    boards = Board.objects.filter(username_id=username)
    tasks = Task.objects.filter(board_id__in=boards)
    board_form = NewBoard(prefix='board')
    task_form = NewTask(prefix='task')
    for board in boards:
        todo_dict[board] = []
    for task in tasks:
        task_dict = {'id': task.id, 'action': task.name, 'done': task.status, 'details': task.details}
        if task_dict['done']:
            todo_dict[task.board].append(task_dict)
        else:
            todo_dict[task.board].insert(index_position, task_dict)
            index_position += 1

    context = {
        'todo_dict': todo_dict,
        'board_form': board_form,
        'task_form': task_form
    }
    return render(request, 'todo.html', context=context)


class SearchResultsView(ListView):
    model = User
    template_name = 'search_results.html'

    def get_queryset(self):
        object_list = []
        if 'searched_item' in self.request.GET:
            query = self.request.GET.get('searched_item')
            object_list = User.objects.filter(username__icontains=query)
        return object_list


@login_required
def change_friendship(request, pk):
    user_id = request.user.id
    if request.method == 'POST':
        user_instance = get_object_or_404(User, pk=user_id)
        friend_instance = get_object_or_404(User, pk=pk)
        friendship_instance, created = Friend.objects.get_or_create(user=user_instance, friend=friend_instance)
        if created:
            friendship_instance.save()
        else:
            friendship_instance.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseNotFound()


