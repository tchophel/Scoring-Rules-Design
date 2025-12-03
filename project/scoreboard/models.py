from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    total_points = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return self.username

class Match(models.Model):
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='upcoming')
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.team1} vs {self.team2} at {self.start_time}'

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team1_prediction = models.IntegerField()
    team2_prediction = models.IntegerField()
    points_earned = models.IntegerField(default=0)
    boost_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Prediction by {self.user.username} for {self.match}'

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='completed')

    def __str__(self):
        return f'Payment of {self.amount} by {self.user.username} on {self.date}'
