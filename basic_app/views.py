from django.shortcuts import render
from basic_app.forms import FlatsForm, OrderForm
from basic_app.models import FlatType, Order, Client
from django.db.models import Q
from django.shortcuts import redirect
from django.db import models
from datetime import datetime

# Create your views here.


def find_client(request):
    return render(request, 'basic_app/html/find_client.html')


def get_clients(discount_card, phone_number):
    return Client.objects.filter(Q(discount_card__exact=discount_card) | Q(phone_number__exact=phone_number))


def client_settlement(request):
    print('hi!')
    clt = Client.objects.filter(Q(discount_card__exact=request.GET["discount_card"]) | Q(phone_number__exact=request.GET["phone_number"]))
    delta = datetime.strptime(request.GET['date_to'], "%Y-%m-%d") - datetime.strptime(request.GET['date_from'],
                                                                                      "%Y-%m-%d")
    days = delta.days
    context = {
        "address": request.GET['address'],
        "discount_card": request.GET["discount_card"],
        "phone_number": request.GET["phone_number"],
        "flag": True,
        "price": (1 + days) * int(request.GET['price']),
    }

    if not clt:
        context["name"] = f"{request.GET['first_name']} {request.GET['last_name']}"
        context["bonuses"] = 0
        context["final_price"] = (1 + days) * int(request.GET['price'])
    else:
        for c in clt:
            context["name"] = c.name
            context["bonuses"] = c.bonuses
            context["final_price"] = (1 + days) * int(request.GET['price']) - c.bonuses

    if request.method == 'POST':
        print('1')
        return render(request, 'basic_app/html/discount_setup.html')
    return render(request, 'basic_app/html/client_settlement.html', context=context)


def add_client(request):
    form = OrderForm()
    context = {'form': form}

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            discount_card = form.cleaned_data['discount_card']
            phone_number = form.cleaned_data['phone_number']
            clients = Client.objects.filter(Q(discount_card__exact=discount_card) | Q(phone_number__exact=phone_number))
            request.POST["add_client"] = {'form': form, 'clients': clients}
            context = {'form': form, 'clients': clients}
            add_client(request)

    return render(request, 'basic_app/html/add_client.html', context=context)


def signin(request):
    return render(request, 'basic_app/html/signin.html')


def discount_setup(request):
    return render(request, 'basic_app/html/discount_setup.html')


def add_flat(request):
    form = FlatsForm()
    context = {'form': form}

    if request.method == 'POST':
        form = FlatsForm(request.POST)

        if form.is_valid():
            flat = form.save(commit=False)
            type_id = int(request.POST.dict()["type"])
            flat.type = FlatType.objects.get(pk=type_id)
            flat.save()
            return render(request, 'basic_app/html/add_flat.html', context=context)
    return render(request, 'basic_app/html/add_flat.html', context=context)


