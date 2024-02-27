from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Investments
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
import datetime
import json
import csv

# Create your views here.

@login_required(login_url='/authentication/login')
def search_investments(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        investments = Investments.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Investments.objects.filter(
            date__istartswith=search_str, owner=request.user) | Investments.objects.filter(
            description__icontains=search_str, owner=request.user) | Investments.objects.filter(
            category__icontains=search_str, owner=request.user)

        data = list(investments.values())

        return JsonResponse(data, safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    investments = Investments.objects.filter(owner=request.user)
    paginator = Paginator(investments, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context ={
        'investments':investments,
        'page_obj': page_obj,
    }

    return render(request, 'investments/index.html', context)

@login_required(login_url='/authentication/login')
def add_investment(request):
    categories = Category.objects.all()
    context = {
            'categories': categories,
            'values': request.POST,
    }

    if request.method=="POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['investment_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Necessário informar um valor!')
            return render(request, 'investments/add_investment.html', context)
    
        if not description:
            messages.error(request, 'Necessário informar uma descrição!')
            return render(request, 'investments/add_investment.html', context)
        
        Investments.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
        messages.success(request, 'Investimento criado com sucesso!')

        return redirect('investments')

    return render(request, 'investments/add_investment.html', context)

@login_required(login_url='/authentication/login')
def investment_edit(request, id):
    investment = Investments.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'investment': investment,
        'values': investment,
        'categories': categories,
    }
    if request.method=="GET":
        return render(request, 'investments/edit-investment.html', context)
        
    if request.method=="POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['investment_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Necessário informar um valor!')
            return render(request, 'investments/edit-investment.html', context)
    
        if not description:
            messages.error(request, 'Necessário informar uma descrição!')
            return render(request, 'investments/edit-investment.html', context)

        investment.owner = request.user
        investment.amount = amount
        investment.date = date
        investment.category = category
        investment.description = description

        investment.save()
        messages.success(request, 'Investimento atualizado com sucesso!')

        return redirect('investments')
    
@login_required(login_url='/authentication/login')
def investment_delete(request, id):
    investment = Investments.objects.get(pk=id)
    investment.delete()
    messages.success(request, 'Investimento removido!')
    return redirect('investments')

@login_required(login_url='/authentication/login')
def investment_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    investments = Investments.objects.filter(owner=request.user)
    finalrep = {}

    def get_category(investment):
        return investment.category
    category_list = list(set(map(get_category, investments)))

    def get_investment_category_amount(category):
        amount = 0
        filtered_by_category = investments.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in investments:
        for y in category_list:
            finalrep[y] = get_investment_category_amount(y)

    return JsonResponse({'investment_category_data': finalrep}, safe=False)

@login_required(login_url='/authentication/login')
def stats_view(request):
    return render(request, 'investments/stats.html')

def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition']='attachment; filename=Investimentos'+str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Quantia', 'Descricao', 'Incorporadora', 'Data'])

    investments = Investments.objects.filter(owner=request.user)

    for investment in investments:
        writer.writerow([investment.amount, investment.description, investment.category, investment.date])

    return response

def export_xlsx(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Investimentos' + str(datetime.datetime.now()) + '.xlsx'

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(['Quantia', 'Descricao', 'Incorporadora', 'Data'])

    investments = Investments.objects.filter(owner=request.user)

    for investment in investments:
        worksheet.append([investment.amount, investment.description, investment.category, investment.date])

    workbook.save(response)

    return response

def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Investimentos' + str(datetime.datetime.now()) + '.pdf'

    p = canvas.Canvas(response)
    p.drawString(100, 800, 'Quantia | Descrição | Incorporadora | Data')

    investments = Investments.objects.filter(owner=request.user)

    y = 780
    for investment in investments:
        y -= 20
        p.drawString(100, y, f'{investment.amount} | {investment.description} | {investment.category} | {investment.date}')

    p.showPage()
    p.save()

    return response


        



