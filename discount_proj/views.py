from django.shortcuts import render


def index(request):
    return render(request, 'basic_app/html/main_page.html')
