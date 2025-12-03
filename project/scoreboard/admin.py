from django.contrib import admin
from .models import User, Match, Prediction, Payment

admin.site.register(User)
admin.site.register(Match)
admin.site.register(Prediction)
admin.site.register(Payment)
