from django.shortcuts import render, redirect
from .forms import NewUserForm, addnewteam, addnewplayer
from django.contrib.auth import login, authenticate  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth import login, authenticate, logout  # add this
from .models import team, player, livematch
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)

global nteam1
global nteam2
global noteam
global matchscore
global current


def home(request):
    global noteam
    noteam = 2
    global matchscore
    context = {}
    context["dataset"] = matchscore
    return render(request, 'home.html', context)


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
    # global numofteam
    # if numofteam:
    #     context = {}
    #     numofteam = numofteam - 1
    #     form = addnewteam(request.POST or None)
    #     if form.is_valid():
    #         form.save()
    #     if numofteam == 0:
    #         form = addnewplayer(request.POST or None)
    #         context['form'] = form
    #         return render(request, "player_name.html", context)
    #     context['form'] = form
    #     return render(request, "create_view.html", context)
    # # context = {}
    # # context["dataset"] = team.objects.all()
    return render(request=request, template_name="team_name_form.html")


def team_name(request):
    global nteam1
    global nteam2
    global noteam
    global matchscore
    global current
    team_name = request.POST.get('team1')
    u = team(teamname=team_name)
    u.save()
    if noteam == 2:
        nteam1 = u
    else:
        nteam2 = u
    noteam = noteam - 1
    player_name = request.POST.get('player1')
    p = player(playername=player_name, team=u)
    p.save()
    player_name = request.POST.get('player2')
    p1 = player(playername=player_name, team=u)
    p1.save()
    player_name = request.POST.get('player3')
    p1 = player(playername=player_name, team=u)
    p1.save()
    player_name = request.POST.get('player4')
    p1 = player(playername=player_name, team=u)
    p1.save()
    player_name = request.POST.get('player5')
    p1 = player(playername=player_name, team=u)
    p1.save()
    player_name = request.POST.get('player6')
    p1 = player(playername=player_name, team=u)
    p1.save()
    player_name = request.POST.get('player7')
    p1 = player(playername=player_name, team=u)
    p1.save()
    player_name = request.POST.get('player8')
    p1 = player(playername=player_name, team=u)
    p1.save()
    player_name = request.POST.get('player9')
    p1 = player(playername=player_name, team=u)
    p1.save()
    player_name = request.POST.get('player10')
    p1 = player(playername=player_name, team=u)
    p1.save()
    player_name = request.POST.get('player11')
    p1 = player(playername=player_name, team=u)
    p1.save()
    context = {}
    # context["dataset"] = player.objects.all()
    # context["dataset2"] = team.objects.all()
    if noteam == 0:
        m1 = livematch(teamname1=nteam1.teamname, teamname2=nteam2.teamname)
        m1.save()
        context["dataset"] = m1
        matchscore = m1
        current = 1
        return render(request, "scoring.html", context)
    else:
        return render(request=request, template_name="team_name_form.html")


def addplayer_name(request):
    global numofteam1
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
    context["dataset"] = player.objects.all()
    return render(request, "list_view.html", context)


def list_view(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
    context["dataset"] = player.objects.all()
    context["dataset2"] = team.objects.all()
    return render(request, "list_view.html", context)


def update_score(request):
    global current
    global matchscore
    context = {}
    context["dataset"] = matchscore
    context["current"] = current
    if 'inning_end' in request.POST:
        current = 2
        matchscore.balls = 120
        matchscore.current_ball = 0
        matchscore.save()
        return render(request, "scoring.html", context)
    if current == 2 and matchscore.score2 > matchscore.score1:
        matchscore.win = 2
        matchscore.save()
        return render(request, "result.html", context)
    elif current == 2 and (matchscore.balls == 0 or matchscore.wicket2 == 10):
        matchscore.win = 1
        matchscore.save()
        return render(request, "result.html", context)
    elif current == 2 and (matchscore.balls == 0 or matchscore.wicket2 == 10) and matchscore.score2 == matchscore.score1:
        return render(request, "result.html", context)

    if current == 1:
        if matchscore.balls == 0 or matchscore.wicket1 == 10:
            current = 2
            return render(request, "scoring.html", context)
        if 'dot' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            if matchscore.current_ball == 7:
                matchscore.over1 = matchscore.over1 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'one' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score1 = matchscore.score1 + 1
            if matchscore.current_ball == 7:
                matchscore.over1 = matchscore.over1 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'two' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score1 = matchscore.score1 + 2
            if matchscore.current_ball == 7:
                matchscore.over1 = matchscore.over1 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'three' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score1 = matchscore.score1 + 3
            if matchscore.current_ball == 7:
                matchscore.over1 = matchscore.over1 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'four' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score1 = matchscore.score1 + 4
            if matchscore.current_ball == 7:
                matchscore.over1 = matchscore.over1 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'five' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score1 = matchscore.score1 + 5
            if matchscore.current_ball == 7:
                matchscore.over1 = matchscore.over1 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'six' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score1 = matchscore.score1 + 6
            if matchscore.current_ball == 7:
                matchscore.over1 = matchscore.over1 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'wicket' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.wicket1 = matchscore.wicket1 + 1
            if matchscore.current_ball == 7:
                matchscore.over1 = matchscore.over1 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'wide' in request.POST:
            matchscore.score1 = matchscore.score1 + 1
            matchscore.save()
            return render(request, "extra_runs.html")
        elif 'noball' in request.POST:
            matchscore.score1 = matchscore.score1 + 1
            matchscore.save()
            return render(request, "extra_runs.html")
        elif 'freehit' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            if matchscore.current_ball == 7:
                matchscore.over1 = matchscore.over1 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "extra_runs.html")
    else:
        if 'dot' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            if matchscore.current_ball == 7:
                matchscore.over2 = matchscore.over2 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'one' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score2 = matchscore.score2 + 1
            if matchscore.current_ball == 7:
                matchscore.over2 = matchscore.over2 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'two' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score2 = matchscore.score2 + 2
            if matchscore.current_ball == 7:
                matchscore.over2 = matchscore.over2 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'three' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score2 = matchscore.score2 + 3
            if matchscore.current_ball == 7:
                matchscore.over2 = matchscore.over2 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'four' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score2 = matchscore.score2 + 4
            if matchscore.current_ball == 7:
                matchscore.over2 = matchscore.over2 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'five' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score2 = matchscore.score2 + 5
            if matchscore.current_ball == 7:
                matchscore.over2 = matchscore.over2 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'six' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.score2 = matchscore.score2 + 6
            if matchscore.current_ball == 7:
                matchscore.over2 = matchscore.over2 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'wicket' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            matchscore.wicket2 = matchscore.wicket2 + 1
            if matchscore.current_ball == 7:
                matchscore.over2 = matchscore.over2 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'wide' in request.POST:
            matchscore.score2 = matchscore.score2 + 1
            matchscore.save()
            return render(request, "extra_runs.html")
        elif 'noball' in request.POST:
            matchscore.score2 = matchscore.score2 + 1
            matchscore.save()
            return render(request, "extra_runs.html")
        elif 'freehit' in request.POST:
            matchscore.balls = matchscore.balls - 1
            matchscore.current_ball = matchscore.current_ball + 1
            if matchscore.current_ball == 7:
                matchscore.over2 = matchscore.over2 + 1
                matchscore.current_ball = 1
            matchscore.save()
            return render(request, "extra_runs.html")


def extrarun(request):
    global matchscore
    global current
    context = {}
    context["dataset"] = matchscore
    if current == 1:
        if 'dot' in request.POST:
            return render(request, "scoring.html", context)
        elif 'one' in request.POST:
            matchscore.score1 = matchscore.score1 + 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'two' in request.POST:
            matchscore.score1 = matchscore.score1 + 2
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'three' in request.POST:
            matchscore.score1 = matchscore.score1 + 3
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'four' in request.POST:
            matchscore.score1 = matchscore.score1 + 4
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'five' in request.POST:
            matchscore.score1 = matchscore.score1 + 5
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'six' in request.POST:
            matchscore.score1 = matchscore.score1 + 6
            matchscore.save()
            return render(request, "scoring.html", context)
    else:
        if 'dot' in request.POST:
            return render(request, "scoring.html", context)
        elif 'one' in request.POST:
            matchscore.score2 = matchscore.score2 + 1
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'two' in request.POST:
            matchscore.score2 = matchscore.score2 + 2
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'three' in request.POST:
            matchscore.score2 = matchscore.score2 + 3
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'four' in request.POST:
            matchscore.score2 = matchscore.score2 + 4
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'five' in request.POST:
            matchscore.score2 = matchscore.score2 + 5
            matchscore.save()
            return render(request, "scoring.html", context)
        elif 'six' in request.POST:
            matchscore.score2 = matchscore.score2 + 6
            matchscore.save()
            return render(request, "scoring.html", context)
