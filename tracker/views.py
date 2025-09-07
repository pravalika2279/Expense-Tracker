from django.shortcuts import render, redirect, get_object_or_404
from tracker.models import TrackHistory,CurrentBalance,Income,Expense
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user= User.objects.filter(username=username)
        if not user.exists():
            messages.error(request,"User not exits, first register to login...")
            return redirect('/register')
        user= authenticate(username=username, password=password)
        if not user:
            messages.error(request,"Incorrect credentials")
            return redirect('/login')
        login(request, user)
        return redirect('/')
    return render(request,'login.html')

def register_view(request):
    if request.method=='POST':
        first_name= request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username= request.POST.get('username')
        password=request.POST.get('password')
        user= User.objects.filter(username=username)
        if user.exists():
            messages.error(request,"User already exists, login to continue...")
            return redirect('/login')
        user= User.objects.create(first_name=first_name, last_name=last_name,email=email, username=username)
        user.set_password(password)
        user.save()
        messages.success(request,"Successfully account created")
        return redirect('/login')
    return render(request,'register.html')

def logout_view(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def index(request):
    current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)
    income, _ = Income.objects.get_or_create(user=request.user)
    expense, _ = Expense.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        expense_type = request.POST.get('expense_type')

        track = TrackHistory.objects.create(
            user=request.user,
            current_balance=current_balance,
            income_money=income,
            expense_money=expense,
            Description=description,
            Amount=amount,
            Expense_Type=expense_type
        )

        income_total = TrackHistory.objects.filter(user=request.user, Expense_Type='CREDIT').aggregate(total=Sum('Amount'))['total'] or 0
        expense_total = TrackHistory.objects.filter(user=request.user, Expense_Type='DEBIT').aggregate(total=Sum('Amount'))['total'] or 0

        income.Income = income_total
        expense.Expense = expense_total
        current_balance.Current_Balance = income_total - expense_total
        if current_balance.Current_Balance < 0:
            current_balance.Current_Balance = 0

        income.save()
        expense.save()
        current_balance.save()

        return redirect('/')

    history = TrackHistory.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'history': history,
        'income': income.Income,
        'expense': expense.Expense,
        'current_balance': current_balance.Current_Balance
    }
    return render(request, 'index.html', context)


"""
@login_required(login_url='/login')
def index(request):
    if request.method=='POST':
        description= request.POST.get('description')
        amount= request.POST.get('amount')
        expense_type= request.POST.get('expense_type')
        current_balance= CurrentBalance.objects.get_or_create(id=1)
        income=Income.objects.get_or_create(id=2)
        expense=Expense.objects.get_or_create(id=3)
        track=TrackHistory.objects.create(user=request.user, current_balance=current_balance[0],income_money=income[0],expense_money=expense[0],Description=description, Amount=amount, Expense_Type=expense_type)
        income_mon=TrackHistory.objects.filter(Expense_Type='CREDIT').aggregate(total=Sum('Amount'))['total']
        expense_mon=TrackHistory.objects.filter(Expense_Type='DEBIT').aggregate(total=Sum('Amount'))['total']
        if income_mon:
            income= Income.objects.get(id=2)
            income.Income=income_mon
            income.save()
        if expense_mon:
            expense=Expense.objects.get(id=3)
            expense.Expense=expense_mon
            expense.save()
        income= Income.objects.get(id=2)
        expense=Expense.objects.get(id=3)
        current_balance= CurrentBalance.objects.get(id=1)
        current_balance.Current_Balance=income.Income-expense.Expense
        if current_balance.Current_Balance<0:
            current_balance.Current_Balance=0
        current_balance.save()
        return redirect('/')
    current_balance= CurrentBalance.objects.get_or_create(id=1)
    income= Income.objects.get_or_create(id=2)
    expense= Expense.objects.get_or_create(id=3)
    history=TrackHistory.objects.all()
    context={'history': history, 'income':income[0].Income, 'expense':expense[0].Expense, 'current_balance':current_balance[0].Current_Balance}
    return render(request,'index.html',context)
"""


@login_required(login_url='/login')
def delete(request, id):
    history = get_object_or_404(TrackHistory, id=id, user=request.user)

    # Delete the record
    history.delete()

    # Recalculate totals after deletion
    income_total = TrackHistory.objects.filter(user=request.user, Expense_Type='CREDIT').aggregate(total=Sum('Amount'))['total'] or 0
    expense_total = TrackHistory.objects.filter(user=request.user, Expense_Type='DEBIT').aggregate(total=Sum('Amount'))['total'] or 0

    income, _ = Income.objects.get_or_create(user=request.user)
    expense, _ = Expense.objects.get_or_create(user=request.user)
    current_balance, _ = CurrentBalance.objects.get_or_create(user=request.user)

    income.Income = income_total
    expense.Expense = expense_total
    current_balance.Current_Balance = income_total - expense_total
    if current_balance.Current_Balance < 0:
        current_balance.Current_Balance = 0

    income.save()
    expense.save()
    current_balance.save()

    return redirect('/')


"""
def delete(request,id):
    history=TrackHistory.objects.get(id=id)
    if history.Expense_Type=="CREDIT":
        history.income_money.Income-=history.Amount
        history.income_money.save()
    else:
        history.expense_money.Expense-=history.Amount
        history.expense_money.save()
    income= Income.objects.get(id=2)
    expense=Expense.objects.get(id=3)
    current_balance= CurrentBalance.objects.get(id=1)
    current_balance.Current_Balance=income.Income-expense.Expense
    if current_balance.Current_Balance<0:
        current_balance.Current_Balance=0
    current_balance.save()
    history.delete()
    return redirect('/')

"""

