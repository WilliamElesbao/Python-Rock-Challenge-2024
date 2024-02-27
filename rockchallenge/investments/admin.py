from django.contrib import admin
from .models import Investments, Category

# Register your models here.

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('amount','date','description','owner','category')
    search_fields = ('description','date','category')

    list_per_page = 5

admin.site.register(Investments, InvestmentAdmin)
admin.site.register(Category)