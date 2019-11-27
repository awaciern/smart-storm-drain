from django.shortcuts import render

def index(request):
    return render(request, 'index.html', context=None)

def user_interface(request):
    return render(request, 'user_interface.html', context=None)
