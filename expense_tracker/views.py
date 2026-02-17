from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm, IncomeForm, SavingsForm, TodoItemForm,BudgetForm,DateRangeForm
from .models import Expense, Income, Saving, TodoItem,Budget
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
import requests
from openpyxl import Workbook
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.dateparse import parse_date
from datetime import timedelta,datetime
#-------------------------------------------------------------LOGIN VIEW-----------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'expense_tracker/login.html', {'error': 'Invalid username or password'})
    return render(request, 'expense_tracker/login.html')
#-------------------------------------------------------------HOME VIEW---------------------------------------------------------------
@login_required
def home_view(request):
    total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_savings = Saving.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_income': total_income,
        'total_savings': total_savings,
        'total_expenses': total_expenses,
    }
    
    return render(request, 'expense_tracker/home.html', context)

#----------------------------------------------------------- ALL VIEWS RELATED TO EXPENSE---------------------------------------------------------
@login_required
def expense_view(request):
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense_form.save()
            return redirect('expense')
    else:
        expense_form = ExpenseForm()

    expenses = Expense.objects.all()
    return render(request, 'expense_tracker/expense.html', {
        'expense_form': expense_form,
        'expenses': expenses
    })
@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense')  # Redirect to the list of expenses after saving
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense_tracker/expense_edit.html', {'form': form})
@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense')  # Redirect to the list of expenses after deleting
    return render(request, 'expense_tracker/expense_confirm_delete.html', {'expense': expense})

@login_required

def export_transactions_xlsx(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=expenses.xlsx'

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Expenses'
    
    worksheet.append(['Date', 'Amount', 'Category', 'Expense Name'])
    
    expenses = Expense.objects.all()
    for expense in expenses:
        worksheet.append([
            expense.date.strftime('%Y-%m-%d'),
            expense.amount,
            expense.category,
            expense.expense_name
        ])
    
    workbook.save(response)
    return response

#----------------------------------------------------------- ALL VIEWS RELATED TO INCOME---------------------------------------------------------
@login_required
def income_view(request):
    if request.method == 'POST':
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            income_form.save()
            return redirect('income')
    else:
        income_form = IncomeForm()

    incomes = Income.objects.all()
    return render(request, 'expense_tracker/income.html', {'income_form': income_form, 'incomes': incomes})

@login_required
def income_edit(request, id):
    income = get_object_or_404(Income, pk=id)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'expense_tracker/income_edit.html', {'form': form})
    
@login_required
def income_delete(request, id):
    income = get_object_or_404(Income, pk=id)
    if request.method == "POST":
        income.delete()
        return redirect('income')
    return render(request, 'expense_tracker/income_confirm_delete.html', {'income': income})

#----------------------------------------------------------- ALL VIEWS RELATED TO SAVINGS---------------------------------------------------------
@login_required
def savings_view(request):
    if request.method == 'POST':
        savings_form = SavingsForm(request.POST)
        if savings_form.is_valid():
            savings_form.save()
            return redirect('savings')
    else:
        savings_form = SavingsForm()

    savings = Saving.objects.all()
    return render(request, 'expense_tracker/savings.html', {'savings_form': savings_form, 'savings': savings})
@login_required
def savings_edit(request, pk):
    saving = get_object_or_404(Saving, pk=pk)
    if request.method == 'POST':
        form = SavingsForm(request.POST, instance=saving)
        if form.is_valid():
            form.save()
            return redirect('savings')
    else:
        form = SavingsForm(instance=saving)
    return render(request, 'expense_tracker/savings_edit.html', {'form': form})

@login_required
def savings_delete(request, pk):
    saving = get_object_or_404(Saving, pk=pk)
    if request.method == 'POST':
        saving.delete()
        return redirect('savings')
    return render(request, 'expense_tracker/savings_confirm_delete.html', {'saving': saving})
def logout_view(request):
    logout(request)
    return redirect('login')
#----------------------------------------------------------- ALL VIEWS RELATED TO DO LIST---------------------------------------------------------
@login_required
def todo_list(request):
    todos = TodoItem.objects.filter(user=request.user)

    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo')
    else:
        form = TodoItemForm()
    
    return render(request, 'expense_tracker/todo_list.html', {'todos': todos, 'form': form})

@login_required
def todo_complete(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    todo.completed = True
    todo.save()
    return redirect('todo')

@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    todo.delete()
    return redirect('todo')
@login_required
def todo_clear_all(request):
    if request.method == 'POST':
        TodoItem.objects.filter(user=request.user).delete()
    return redirect('todo')
#----------------------------------------------------------- CALCULATOR---------------------------------------------------------
@login_required
def calculator_view(request):
    if request.method == 'POST':
        num1 = int(request.POST['num1'])
        num2 = int(request.POST['num2'])
        operator = request.POST['operator']

        if operator == 'add':
            result = num1 + num2
        elif operator == 'subtract':
            result = num1 - num2
        elif operator == 'multiply':
            result = num1 * num2
        elif operator == 'divide':
            if num2 != 0:
                result = num1 / num2
            else:
                return HttpResponse("Error: Division by zero!")

        return render(request, 'expense_tracker/calculator.html', {'result': result})

    return render(request, 'expense_tracker/calculator.html')


#----------------------------------------------------------- ALL VIEWS RELATED TO CURRENCY CONVERTER---------------------------------------------------------
API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'
def get_exchange_rates():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data['rates']
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {}

def convert_currency(amount, from_currency, to_currency):
    rates = get_exchange_rates()
    if not rates:
        return None
    if from_currency != 'USD':
        amount /= rates.get(from_currency, 1)  # Default to 1 if currency not found
    return round(amount * rates.get(to_currency, 1), 2)  # Default to 1 if currency not found

def currency_converter(request):
    converted_amount = None
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount', 0))
            from_currency = request.POST.get('from_currency', 'USD')
            to_currency = request.POST.get('to_currency', 'USD')
            converted_amount = convert_currency(amount, from_currency, to_currency)
        except (ValueError, KeyError) as e:
            # Log or handle the exception as needed
            print(f"Error: {e}")

    return render(request, 'expense_tracker/currency_converter.html', {'converted_amount': converted_amount})
#----------------------------------------------------ALL VIEWS RELATED TO BUDGET PLANNER---------------------------------------
class BudgetListView(ListView):
    model = Budget
    template_name = 'expense_tracker/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).order_by('-created_at')

class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'expense_tracker/budget_form.html'
    success_url = reverse_lazy('budget-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'expense_tracker/budget_update_form.html'  # Template for updating
    success_url = reverse_lazy('budget-list')  # Redirect URL after success

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Budget entry has been updated.')
        return response
class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'expense_tracker/budget_confirm_delete.html'
    success_url = reverse_lazy('budget-list')  # Adjust this to your desired URL name

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Budget entry has been deleted.')
        return super().delete(request, *args, **kwargs)    
    
#-----------------------------------------monthly data view------------------------    
def monthly_report(request):
    form = DateRangeForm(request.POST or None)
    income_total = 0
    expense_total = 0
    savings_total = 0
    transaction=0
    
    if request.method == 'POST' and form.is_valid():
        year = form.cleaned_data['year']
        month = form.cleaned_data['month']
        start_date = datetime(year=int(year), month=int(month), day=1)
        
        # Calculate end_date as the first day of the next month
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
        
        income_total = Income.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
        expense_total = Expense.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
        savings_total = Saving.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
        transaction = income_total+savings_total-expense_total 
    return render(request, 'expense_tracker/monthly_report.html', {
        'form': form,
        'income_total': income_total,
        'expense_total': expense_total,
        'savings_total': savings_total,
        'transaction':transaction,
    })