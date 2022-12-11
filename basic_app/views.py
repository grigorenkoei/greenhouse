from django.shortcuts import render
from basic_app.forms import FlatsForm, OrderForm
from basic_app.models import FlatType

# Create your views here.


def find_client(request):
    return render(request, 'basic_app/html/find_client.html')


def add_client(request):
    form = OrderForm()
    context = {'form': form}

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["date_from"])
            return render(request, 'basic_app/html/add_client.html', context=context)

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


