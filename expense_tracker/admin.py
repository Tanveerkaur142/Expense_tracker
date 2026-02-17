from django.contrib import admin
from . models import Expense,Income,Saving,TodoItem,calculator,Transaction,Budget
from django.utils.translation import gettext_lazy as _

admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(Saving)
admin.site.register(TodoItem)
admin.site.register(calculator)
admin.site.register(Transaction)
admin.site.register(Budget)


admin.site.site_header = "Expense Tracker Admin"
admin.site.site_title = "Expense Tracker Admin Portal"
admin.site.index_title = "Welcome to the Expense Tracker Admin"
