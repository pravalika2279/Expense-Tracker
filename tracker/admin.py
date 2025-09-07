from django.contrib import admin
from tracker.models import *
# Register your models here.

admin.site.register(TrackHistory)
admin.site.register(CurrentBalance)
admin.site.register(Income)
admin.site.register(Expense)