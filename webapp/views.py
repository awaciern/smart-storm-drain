from django.shortcuts import render
from .models import Device, Transmission
from .forms import SelectionForm

def index(request):
    # Initially select the water depth of the first device in the database
    metric = 'depth'
    form = SelectionForm(initial = {'device': Device.objects.first(),
                                    'metric': 'depth'})
    device = Device.objects.first()
    transmissions = Transmission.objects.filter(device=device)

    # Once user selects a device, display its data
    if request.method == 'POST':
        metric = request.POST.get('metric')
        device_id = request.POST.get('device')
        form = SelectionForm(initial = {'device': device_id, 'metric': metric})
        device = Device.objects.get(pk=device_id)
        transmissions = Transmission.objects.filter(device=device)

    # Render the html template with the necessary data passed in
    return render(request, 'index.html', {'form': form,
                                          'metric': metric,
                                          'device': device,
                                          'transmissions': transmissions})

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
