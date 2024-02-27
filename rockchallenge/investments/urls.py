from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index, name='investments'),
    path('add-investment',views.add_investment, name='add-investments'),
    path('edit-investment/<int:id>',views.investment_edit, name='investment-edit'),
    path('investment-delete/<int:id>',views.investment_delete, name='investment-delete'),
    path('search-investments/',csrf_exempt(views.search_investments), name='search_investments'),
    path('investment_category_summary', views.investment_category_summary, name='investment_category_summary'),
    path('stats', views.stats_view, name='stats'),
    path('export_csv', views.export_csv, name='export-csv'),
    path('export_xlsx', views.export_xlsx, name='export-xlsx'),
    path('export_pdf', views.export_pdf, name='export-pdf'),
]