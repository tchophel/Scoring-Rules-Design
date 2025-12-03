from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm, PredictionForm
from .models import User, Match, Prediction

@login_required
def my_predictions(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            match_id = request.POST.get('match_id')
            match = Match.objects.get(id=match_id)
            Prediction.objects.update_or_create(
                user=request.user,
                match=match,
                defaults={
                    'team1_prediction': form.cleaned_data['team1_prediction'],
                    'team2_prediction': form.cleaned_data['team2_prediction'],
                }
            )
            return redirect('my_predictions')
    else:
        form = PredictionForm()

    predictions = Prediction.objects.filter(user=request.user)
    upcoming_matches = Match.objects.filter(status='upcoming')

    predictions_map = {p.match.id: p for p in predictions}

    context = {
        'form': form,
        'upcoming_matches': upcoming_matches,
        'predictions_map': predictions_map,
    }
    return render(request, 'scoreboard/my_predictions.html', context)

def matches(request):
    matches = Match.objects.all()
    return render(request, 'scoreboard/matches.html', {'matches': matches})

def leaderboard(request):
    users = User.objects.order_by('-total_points')
    return render(request, 'scoreboard/leaderboard.html', {'users': users})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('leaderboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'scoreboard/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('leaderboard')
    else:
        form = LoginForm()
    return render(request, 'scoreboard/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('leaderboard')
