from django.shortcuts import render, redirect
from .forms import NewUserForm, addnewteam, addnewplayer
from django.contrib.auth import login, authenticate  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth import login, authenticate, logout  # add this
from .models import team, player
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)

global numofteam
global numofplayer


def home(request):
    global numofteam
    global numofplayer
    numofplayer = 2
    numofteam = 3
    return render(request, 'home.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("cricket:home")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as {username}.")
                return redirect("cricket:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("cricket:home")


def addnewmatch(request):
    global numofteam
    if numofteam:
        context = {}
        numofteam = numofteam - 1
        form = addnewteam(request.POST or None)
        if form.is_valid():
            form.save()
        if numofteam == 0:
            return redirect("cricket:player_name")
        context['form'] = form
        return render(request, "create_view.html", context)
    # context = {}
    # context["dataset"] = team.objects.all()
    return redirect("cricket:player_name")


def addplayer_name(request):
    global numofplayer
    if numofplayer:
        context = {}
        numofplayer = numofplayer - 1
        form = addnewplayer(request.POST or None)
        if form.is_valid():
            form.save()
        context['form'] = form
        return render(request, "player_name.html", context)
    context = {}
# add the dictionary during initialization
    context["dataset"] = team.objects.all()
    return render(request, "list_view.html", context)


def list_view(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
# add the dictionary during initialization
    context["dataset"] = team.objects.all()
    return render(request, "list_view.html", context)
