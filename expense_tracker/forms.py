from django import forms
from django.forms import ModelForm
from .models import Expense,Income,Saving,TodoItem,Budget
from django.utils.dateparse import parse_date
from datetime import datetime

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = {'expense_name','amount','category','date'}



class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = {'income_source','amount','date'}  



class SavingsForm(ModelForm):
    class Meta:
        model= Saving
        fields = {'saving_name','amount','date'}



class TodoItemForm(ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'completed']




class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'time_frame', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DateRangeForm(forms.Form):

    YEAR_CHOICES = [(year, year) for year in range(2020, 2040)]
    
    MONTH_CHOICES = [
        ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
        ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
        ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ]

    year = forms.ChoiceField(choices=YEAR_CHOICES)
    month = forms.ChoiceField(choices=MONTH_CHOICES)

    def get_month_display(self):
        month_number = self.cleaned_data.get('month')
        return dict(self.MONTH_CHOICES).get(month_number, 'Unknown Month')