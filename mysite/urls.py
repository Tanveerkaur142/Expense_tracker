"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from expense_tracker import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('expense/', views.expense_view, name='expense'),
    path('expense/edit/<int:pk>/', views.expense_edit, name='expense_edit'),
    path('expense/delete/<int:pk>/', views.expense_delete, name='expense_delete'),
    path('export/xlsx/', views.export_transactions_xlsx, name='export_transactions_xlsx'),
    path('income/', views.income_view, name='income'),
    path('income/<int:id>/edit/', views.income_edit, name='income_edit'),
    path('income/<int:id>/delete/', views.income_delete, name='income_delete'),
    path('savings/', views.savings_view, name='savings'), 
    path('savings/edit/<int:pk>/', views.savings_edit, name='savings_edit'),
    path('savings/delete/<int:pk>/', views.savings_delete, name='savings_delete'),
    path('todo/', views.todo_list, name='todo'),
    path('todo/complete/<int:todo_id>/', views.todo_complete, name='todo_complete'),
    path('todo/delete/<int:pk>/', views.todo_delete, name='todo_delete'),
    path('todo/clear_all/', views.todo_clear_all, name='todo_clear_all'),
    path('calculator/', views.calculator_view, name='calculator'),
    path('currency-converter/', views.currency_converter, name='currency_converter'),
    path('budgets/', views.BudgetListView.as_view(), name='budget-list'),
    path('budgets/new/',views. BudgetCreateView.as_view(), name='budget-create'),
    path('budgets/<int:pk>/edit/',views.BudgetUpdateView.as_view(), name='budget-update'),
    path('budget/delete/<int:pk>/', views.BudgetDeleteView.as_view(), name='budget-delete'),
    path('monthly-report/',views.monthly_report, name='monthly-report')
]
