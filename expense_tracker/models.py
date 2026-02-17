from django.db import models
from django.contrib.auth.models import User
from django import forms

class Expense(models.Model):
    expense_name = models.CharField(max_length=200)
    amount = models.FloatField()
    category = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return self.expense_name
    
class Income(models.Model):
    income_source = models.CharField(max_length=200)
    amount = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.income_source
     
class Saving(models.Model):
    saving_name = models.CharField(max_length=200)
    amount = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.saving_name     
    


class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class calculator (models.Model):
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    operator = models.CharField(max_length=10)  # e.g., 'add', 'subtract', etc.
    result = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.num1} {self.operator} {self.num2} = {self.result}" 
    

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    expense_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField() 


class Budget(models.Model):
    TIME_FRAME_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_frame = models.CharField(max_length=10, choices=TIME_FRAME_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.time_frame} Budget for {self.user.username}"    