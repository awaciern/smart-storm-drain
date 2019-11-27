from django.shortcuts import render

def index(request):
    return render(request, 'index.html', context=None)

def ui(request):
    return render(request, 'ui.html', context=None)
