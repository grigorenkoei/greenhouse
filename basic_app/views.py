from django.shortcuts import render
from basic_app.forms import FlatsForm, OrderForm
from basic_app.models import FlatType, Order, Client, OrderStatus, Flat
from django.db.models import Q
from django.shortcuts import redirect
from django.db import models
from datetime import datetime
import pytz

# Create your views here.


def find_client(request):
    return render(request, 'basic_app/html/find_client.html')


def get_clients(discount_card, phone_number):
    return Client.objects.filter(Q(discount_card__exact=discount_card) | Q(phone_number__exact=phone_number))


def success(request):
    return render(request, 'basic_app/html/success.html')


def create_order(context):
    if context["is_new_client"]:
        client = Client(name=f'{context["first_name"]} {context["last_name"]}',
                        discount_card=context["discount_card"],
                        phone_number=context["phone_number"],
                        desc=context["desc"],
                        bonuses=0)
        client.save()
    else:
        client = get_clients(discount_card=context["discount_card"], phone_number=context["phone_number"]).first()

    order_status = OrderStatus.objects.get(order_status_name='Active')
    flat = Flat.objects.get(pk=int(context["address"]))
    order = Order(client=client,
                  date_from=datetime.strptime(context["date_from"], "%Y-%m-%d").date(),
                  date_to=datetime.strptime(context["date_to"], "%Y-%m-%d").date(),
                  flat=flat,
                  price=int(context["price"]),
                  bonuses_used=int(context["bonuses_used"]),
                  order_status=order_status)
    order.save()


def add_client(request):
    if request.method == "GET":
        form = OrderForm(request.GET or None)
        context = {'form': form}
        if form.is_valid():
            clt = get_clients(request.GET["discount_card"], request.GET["phone_number"])
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
                request.session["bonuses_used"] = 0
                request.session["is_new_client"] = True
            else:
                context["name"] = clt.first().name
                context["bonuses"] = clt.first().bonuses
                sum_price = (1 + days) * int(request.GET['price'])
                if clt.first().bonuses > sum_price:
                    request.session["bonuses_used"] = sum_price
                else:
                    request.session["bonuses_used"] = clt.first().bonuses
                context["final_price"] = (1 + days) * int(request.GET['price']) - request.session["bonuses_used"]
                request.session["is_new_client"] = False
            return render(request, 'basic_app/html/client_settlement.html', context=context)
        else:
            return render(request, 'basic_app/html/add_client.html', context=context)
    else:
        if request.method == 'POST':
            context = request.GET.copy()
            context["is_new_client"] = request.session["is_new_client"]
            context["bonuses_used"] = request.session["bonuses_used"]
            create_order(context)
            return redirect('/basic_app/success')


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
