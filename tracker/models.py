from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CurrentBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Current_Balance= models.FloatField(default=0.0)

class Income(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Income= models.FloatField(default=0.0)

class Expense(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Expense= models.FloatField(default=0.0)

class TrackHistory(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    current_balance= models.ForeignKey(CurrentBalance, on_delete=models.CASCADE, null=True, blank=True)
    income_money= models.ForeignKey(Income,on_delete=models.CASCADE,null=True, blank=True)
    expense_money=models.ForeignKey(Expense,on_delete=models.CASCADE, null=True, blank=True)
    Description=models.CharField(max_length=500)
    Amount= models.FloatField()
    Expense_Type= models.CharField(max_length=200)
