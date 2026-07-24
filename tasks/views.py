from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm, Registerform, TaskCreateForm
import json
from django.core.serializers.json import DjangoJSONEncoder


def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already Signed in')
        return redirect('home')

    form = Registerform()
    errors = None

    if request.method == "POST":
        form = Registerform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Account Created and Login Successful')
                return redirect('home')
            else:
                messages.error(request, 'Invalid Username or Password')
                return redirect('login')
        else:
            errors = form.errors.as_data()
            messages.error(request, errors)
            return redirect('register')

    context = {
        'form': form,
        'errors': errors
    }
    return render(request, 'register.html', context)


@login_required(login_url='login')
def home(request):
    date = datetime.now()
    h = int(date.strftime('%H'))

    msg = 'Good '
    if h < 12:
        msg += 'morning'
    elif h < 16:
        msg += 'afternoon'
    elif h < 18:
        msg += 'evening'
    else:
        msg += 'night'

    greeting = f'{msg}! {request.user.username}'
    tasks = Task.objects.filter(user=request.user).order_by('created_at')
    
    task_data = [
    {'id': t.id, 'title': t.title, 'due_time': t.due_time, 'done': t.done}
    for t in tasks if t.due_time
]
    context = {
        'greeting': greeting,
        'tasks': tasks,
        'task_data_json': json.dumps(task_data, cls=DjangoJSONEncoder)
    }
    return render(request, 'home.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'login successful')
            return redirect('home')
        else:
            messages.error(request, 'We do not know you, please register')
            return redirect("login")

    return render(request, 'login.html')


def logout_view(request):
    messages.success(request, 'You have been successfully logged out.')
    logout(request)
    return redirect('login')




@login_required(login_url='login')
def add_task(request):
    forms = TaskCreateForm()
    if request.method == 'POST':
        forms = TaskCreateForm(request.POST)

        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
            return redirect('add_task')

    context = {
        'forms': forms
    }
    return render(request, "add_task.html", context)

@login_required(login_url='login')
def toggle_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.done = not task.done
    task.save()
    return redirect('home')

@login_required(login_url='login')
def filter_tasks(request, foo):
    if foo == "true":
        tasks = Task.objects.filter(done=True, user=request.user).order_by('-created_at')
    elif foo == 'false':
        tasks = Task.objects.filter(done=False, user=request.user).order_by('-updated_at')
    else:
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'tasks': tasks
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your task update has been made')
            return redirect('home')
        else:
            return redirect('task', pk=pk)

    context = {
        'task': task,
        'form': form
    }
    return render(request, 'update_task.html', context)


@login_required(login_url='login')
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task_title = getattr(task, 'title', 'Task')

    task.delete()
    messages.success(request, f'"{task_title}" was successfully deleted.')
    return redirect('home')