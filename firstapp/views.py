from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserUpdateForm, TodoForm, PasswordUpdateForm
from django.contrib.auth import update_session_auth_hash
from .models import User, Todo
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.
@login_required(login_url="login")
def home(request):
    # todos = Todo.objects.raw("SELECT * FROM firstapp_todo "
    #                          "ORDER BY updated DESC, created DESC")
    q = request.GET.get("search-input") if request.GET.get("search-input") is not None else ""
    todos = Todo.objects.filter(
        Q(name__icontains=q) |
        Q(name__startswith=q)
    )
    count = Todo.objects.filter(user=request.user, completed=False).count()
    context = {"todos": todos, "count": count, "page": "home"}
    return render(request, "firstapp/index.html", context)


@login_required(login_url="login")
def createTodo(request):
    form = TodoForm()
    if request.method == "POST":
        if request.POST.get("completed") == "on":
            completed_v = True
        else:
            completed_v = False
        todo_name = request.POST.get("name")
        Todo.objects.create(
            user=request.user,
            name=todo_name,
            completed=completed_v
        )
        return redirect("home")

    context = {"form": form}
    return render(request, "firstapp/todo_form.html", context)


@login_required(login_url="login")
def updateTodo(request, pk):
    todo = Todo.objects.get(id=pk)
    form = TodoForm(instance=todo)

    if request.method == "POST":
        todo.name = request.POST.get("name")
        if request.POST.get("completed") == "on":
            todo.completed = True
        else:
            todo.completed = False
        todo.save()
        return redirect("home")
    context = {"form": form}
    return render(request, "firstapp/todo_update.html", context)


@login_required(login_url="login")
def deleteTodo(request, pk):
    todo = Todo.objects.get(id=pk)
    if request.method == "POST":
        todo.delete()
        return redirect("home")
    context = {"object": todo}
    return render(request, "firstapp/todo_delete.html", context)


@login_required(login_url="login")
def aboutPage(request):
    return render(request, "firstapp/about.html")


def loginPage(request):
    # if auth-d /login is not allowed
    if request.user.is_authenticated:
        return redirect("home")

    # gets data from form on /login
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        try:
            # check if exists in DB
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist!")

        # if exists then authenticate, check password and username
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # if matches then login the user
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Wrong username or password!")
    return render(request, "firstapp/signin.html")


def registerUser(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = request.POST.get("email").lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration!")

    context = {"form": form}
    return render(request, "firstapp/signup.html", context)


@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserUpdateForm(instance=user)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if request.POST.get("avatar"):
                user.avatar = request.POST.get("avatar")
            user.username = request.POST.get("email")
            user.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "firstapp/user_update.html", context)


@login_required(login_url="login")
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    if request.method == "POST":
        user.delete()
        return redirect("login")
    context = {"object": user}
    return render(request, "firstapp/user_delete.html", context)


@login_required(login_url="login")
def updatePassword(request):
    if request.method == "POST":
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("user_update")
        else:
            messages.error(request, "Please correct the error above.")
    else:
        form = PasswordUpdateForm(request.user)
    return render(request, "firstapp/password_update.html", {'form': form})


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("home")
