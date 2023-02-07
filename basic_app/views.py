from django.shortcuts import render
from basic_app.forms import FlatsForm, OrderForm, ClientSearchForm
from basic_app.models import FlatType, Order, Client, Flat
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import models
from datetime import datetime
import pytz

# Create your views here.


def calculate_bonuses(date_from, date_to, price, bonuses_used=0):
    delta = date_to - date_from
    days = delta.days
    return int((days * price - bonuses_used) * 0.05)


@login_required
def delete_order(request, id):
    order = Order.objects.select_related('client').get(pk=id)
    client = order.client
    all_client_orders = Order.objects.filter(client=client)

    if all_client_orders.count() > 1:
        bonuses_used = order.bonuses_used
        bonuses_accrued = calculate_bonuses(order.date_from, order.date_to, order.price, bonuses_used)
        client.bonuses += bonuses_used - bonuses_accrued

        client.save()
        order.delete()
        return render(request, 'basic_app/html/success.html')
    else:
        order.delete()
        client.delete()
        return render(request, 'basic_app/html/success.html')


@login_required
def find_client(request):
    form = ClientSearchForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        form = ClientSearchForm(request.GET)
        context = {'form': form}
        if len(request.GET["discount_card"]):
            clt = Client.objects.filter(discount_card__exact=request.GET["discount_card"]).first()
        else:
            clt = Client.objects.filter(phone_number__exact=request.GET["phone_number"]).first()

        orders = Order.objects.filter(client__exact=clt)

        context['orders'] = orders
        context['client'] = clt
        print(orders)
        return render(request, 'basic_app/html/client_orders.html', context=context)

    return render(request, 'basic_app/html/find_client.html', context=context)


def get_clients(discount_card, phone_number):
    return Client.objects.filter(Q(discount_card__exact=discount_card) | Q(phone_number__exact=phone_number))


@login_required
def success(request):
    return render(request, 'basic_app/html/success.html')


def create_order(context):
    if context["is_new_client"]:
        client = Client(name=f'{context["first_name"]} {context["last_name"]}',
                        discount_card=context["discount_card"],
                        phone_number=context["phone_number"],
                        desc=context["desc"],
                        bonuses=0)
        bonuses_used = 0
    else:
        client = get_clients(discount_card=context["discount_card"],
                             phone_number=context["phone_number"]).first()
        client.desc += '\n' + context["desc"]
        if int(context["bonuses_selected"]) > int(context["all_client_bonuses"]):
            bonuses_used = int(context["all_client_bonuses"])
            client.bonuses -= bonuses_used
        else:
            bonuses_used = int(context["bonuses_selected"])
            client.bonuses = int(context["all_client_bonuses"]) - bonuses_used

    add_bonuses = calculate_bonuses(datetime.strptime(context["date_from"], "%Y-%m-%d").date(),
                                    datetime.strptime(context["date_to"], "%Y-%m-%d").date(),
                                    int(context["price"]),
                                    bonuses_used)
    client.bonuses += add_bonuses
    client.save()

    flat = Flat.objects.get(pk=int(context["address"]))
    order = Order(client=client,
                  date_from=datetime.strptime(context["date_from"], "%Y-%m-%d").date(),
                  date_to=datetime.strptime(context["date_to"], "%Y-%m-%d").date(),
                  flat=flat,
                  price=int(context["price"]),
                  bonuses_used=int(bonuses_used),
                  bonuses_accrued=add_bonuses)
    order.save()


@login_required
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
                "discount_card": request.GET['discount_card'],
                "phone_number": request.GET['phone_number'],
                "flag": True,
                "price": days * int(request.GET['price']),
            }
            if not clt:
                context["name"] = f"{request.GET['first_name']} {request.GET['last_name']}"
                context["bonuses"] = 0
                request.session["is_new_client"] = True

            else:
                context["name"] = clt.first().name
                context["bonuses"] = clt.first().bonuses
                context["discount_card"] = clt.first().discount_card
                context["phone_number"] = clt.first().phone_number
                request.session["is_new_client"] = False
                request.session["all_client_bonuses"] = clt.first().bonuses
            return render(request, 'basic_app/html/client_settlement.html', context=context)
        else:
            return render(request, 'basic_app/html/add_client.html', context=context)
    else:
        if request.method == 'POST':
            context = request.GET.copy()
            post_context = request.POST.copy()
            print(post_context)
            context["all_client_bonuses"] = request.session["all_client_bonuses"]
            context["bonuses_selected"] = post_context["bonuses_selected"]
            context["is_new_client"] = request.session["is_new_client"]
            create_order(context)
            return redirect('/basic_app/success')


def user_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return HttpResponse('Invalid login or password')
        else:
            return HttpResponse('Invalid login or password')
    return render(request, 'basic_app/html/login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return redirect("/")


@login_required
def discount_setup(request):
    return render(request, 'basic_app/html/discount_setup.html')


@login_required
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
