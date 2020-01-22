from django.shortcuts import render
from datetime import datetime, timezone, timedelta
from .models import Device, Transmission
from .forms import SelectionForm

def index(request):
    # Initially select most recent day's water depth of first device in db
    metric = 'depth'
    form = SelectionForm(initial = {'device': Device.objects.first(),
                                    'metric': 'depth'})
    device = Device.objects.first()
    dates = {}
    dates['start_day'] = Transmission.objects.filter(device=device)\
                                     .last().timestamp.astimezone(tz=None)
    dates['end_day'] = dates['start_day']
    dates['max_day'] = dates['start_day']
    dates['min_day'] = Transmission.objects.filter(device=device)\
                                   .first().timestamp.astimezone(tz=None)
    dt1 = datetime(dates['start_day'].year, dates['start_day'].month,
                         dates['start_day'].day)
    dt2 = datetime(dates['start_day'].year, dates['start_day'].month,
                         dates['start_day'].day) + timedelta(days=1)
    transmissions = Transmission.objects.filter(device=device,
                                                timestamp__range=(dt1, dt2))

    # Once user selects a device, metric, and date range; display its data
    if request.method == 'POST':
        print(request.POST)
        metric = request.POST.get('metric')
        device_id = request.POST.get('device')
        start_day_raw = request.POST.get('from').split('/')
        dates['start_day'] = datetime(int(start_day_raw[2]),
                                      int(start_day_raw[0]),
                                      int(start_day_raw[1]))
        end_day_raw = request.POST.get('to').split('/')
        dates['end_day'] = datetime(int(end_day_raw[2]),
                                    int(end_day_raw[0]),
                                    int(end_day_raw[1]))
        dt1 = dates['start_day']
        dt2 = dates['end_day'] + timedelta(days=1)
        form = SelectionForm(initial = {'device': device_id, 'metric': metric})
        device = Device.objects.get(pk=device_id)
        transmissions = Transmission.objects.filter(device=device,
                                                    timestamp__range=(dt1, dt2))
        print(dates)

    # Render the html template with the necessary data passed in
    return render(request, 'index.html', {'form': form,
                                          'metric': metric,
                                          'device': device,
                                          'dates': dates,
                                          'transmissions': transmissions})

def ui(request):
    return render(request, 'ui.html', context=None)
