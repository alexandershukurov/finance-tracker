from django.contrib import admin
from .models import Status, Type, Category, Subcategory, CashflowEntry

admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(CashflowEntry)