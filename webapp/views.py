from django.shortcuts import render
from .models import Transmission
# from .forms import MessageForm

def index(request):
    transmissions = Transmission.objects.all()

    return render(request, 'index.html', {'transmissions': transmissions})

def ui(request):
    return render(request, 'ui.html', context=None)



# def db(request, choice):
#     return render(request, 'ui.html', context=None)
#
#     if choice == 'none':
#         messages = Message.objects.none()
#     elif choice == 'all':
#         messages = Message.objects.all()
#     elif choice == 'first':
#         earliest = Message.objects.earliest('date')
#         messages = Message.objects.filter(date=earliest.date)
#     elif choice == 'last':
#         latest = Message.objects.latest('date')
#         messages = Message.objects.filter(date=latest.date)
#
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save()
#     else:
#         form = MessageForm()
#
#     return render(request, 'db.html', {'form': form, 'messages': messages})
