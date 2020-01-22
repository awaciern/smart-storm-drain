from django.shortcuts import render
from datetime import datetime, timezone
from .models import Device, Transmission
from .forms import SelectionForm

def index(request):
    # Initially select most recent day's water depth of first device in db
    metric = 'depth'
    form = SelectionForm(initial = {'device': Device.objects.first(),
                                    'metric': 'depth'})
    device = Device.objects.first()
    dates = {}
    dates['start_day'] = Transmission.objects.filter(device=device).last().timestamp.astimezone(tz=None)
    dates['end_day'] = dates['start_day']
    dates['max_day'] = dates['start_day']
    dates['min_day'] = Transmission.objects.filter(device=device).first().timestamp.astimezone(tz=None)
    transmissions = Transmission.objects.filter(device=device)

    # Once user selects a device, display its data
    if request.method == 'POST':
        print(request.POST)
        metric = request.POST.get('metric')
        device_id = request.POST.get('device')
        form = SelectionForm(initial = {'device': device_id, 'metric': metric})
        device = Device.objects.get(pk=device_id)
        transmissions = Transmission.objects.filter(device=device)

    # Render the html template with the necessary data passed in
    return render(request, 'index.html', {'form': form,
                                          'metric': metric,
                                          'device': device,
                                          'dates': dates,
                                          'transmissions': transmissions})

def ui(request):
    return render(request, 'ui.html', context=None)
