from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from .models import Expense, Budget
from .forms import ExpenseForm, BudgetForm

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    today = date.today()
    monthly_expenses = expenses.filter(date__year=today.year, date__month=today.month)
    monthly_total = monthly_expenses.aggregate(total=Sum('amount'))['total'] or 0

    category_totals = (
        monthly_expenses.values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    budget, _ = Budget.objects.get_or_create(user=request.user)
    percent_used = round((monthly_total / budget.monthly_limit) * 100) if budget.monthly_limit else 0

    context = {
        'expenses': expenses,
        'monthly_total': monthly_total,
        'category_totals': list(category_totals),
        'budget': budget,
        'percent_used': min(percent_used, 100),
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

@login_required
def set_budget(request):
    budget, _ = Budget.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'set_budget.html', {'form': form})

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})