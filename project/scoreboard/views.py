from django.shortcuts import render
from .models import User

def leaderboard(request):
    users = User.objects.order_by('-total_points')
    return render(request, 'scoreboard/leaderboard.html', {'users': users})
