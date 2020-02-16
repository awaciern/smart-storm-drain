from django.shortcuts import render
from datetime import datetime, timedelta
from pytz import timezone
from .models import Device, Transmission
from .forms import SelectionForm

def index(request):
    # Create geological and health locations dict
    locations = {}
    for loc in Device.objects.all():
        # Eventually, there will be logic here to determine health from metrics
        # Right now, I am just assigning them
        loc_health = 0
        if loc.pk == 1:
            loc_health = 0
        elif loc.pk == 2:
            loc_health = 1
        elif loc.pk == 3:
            loc_health = 3

        # Assign values to dict
        locations[loc] = {'latitude': loc.latitude, 'longitude': loc.longitude,
                          'health': loc_health}

    # Create overall health dict
    health = {}
    # Eventually, there will be logic here to determine health from metrics
    # Right now, I am just assigning values
    health['overall'] = 2
    health['healthy'] = 1
    health['flowing'] = 1
    health['clogged'] = 0
    health['offline'] = 1

    # Initialize empty date dict
    dates = {}

    # If user selects a device/metric/date range, display proper data
    if request.method == 'POST':
        d = request.POST.get('datetimes').split('-')[0]

        # POST data from python form
        metric = request.POST.get('metric')
        device = Device.objects.get(pk=request.POST.get('device'))

        # POST date data from JS form requiring processing
        date_list_raw = request.POST.get('datetimes').split('-')
        dates['start_day'] = datetime.strptime(date_list_raw[0],
                                               '%m/%d/%y %I:%M %p ')\
                                     .replace(tzinfo=timezone('UTC'))\
                                     - timedelta(hours=19)
        dates['end_day'] = datetime.strptime(date_list_raw[1],
                                             ' %m/%d/%y %I:%M %p')\
                                   .replace(tzinfo=timezone('UTC'))\
                                   - timedelta(hours=19)

        # Find max and min transmission dates based on device selected
        dates['max_day'] = Transmission.objects.filter(device=device)\
                                       .last().timestamp
        dates['min_day'] = Transmission.objects.filter(device=device)\
                                       .first().timestamp

        # Start date is past last transission -> display most recent day data
        if dates['start_day'] > dates['max_day']:  # message???
            dates['end_day'] = Transmission.objects.filter(device=device)\
                                                   .last().timestamp
            dates['start_day'] = datetime(dates['end_day'].year,
                                         dates['end_day'].month,
                                         dates['end_day'].day,
                                         tzinfo=timezone('UTC'))\
                                         - timedelta(hours=19)

        # End date is before first transission -> display most recent day data
        if dates['end_day'] < dates['min_day']:  # message???
            dates['end_day'] = Transmission.objects.filter(device=device)\
                                                   .last().timestamp
            dates['start_day'] = datetime(dates['end_day'].year,
                                          dates['end_day'].month,
                                          dates['end_day'].day,
                                          tzinfo=timezone('UTC'))\
                                          - timedelta(hours=19)

    # User has not yet submitted data; is initially visiting the page
    else:
        # Initially select water depth of first device in db
        metric = 'depth'
        device = Device.objects.first()

        # Initially set date range of most recent day's data
        dates['end_day'] = Transmission.objects.filter(device=device).last()\
                                               .timestamp
        dates['start_day'] = datetime(dates['end_day'].year,
                                      dates['end_day'].month,
                                      dates['end_day'].day,
                                      tzinfo=timezone('UTC'))\
                                      - timedelta(hours=19)
        # Find min transmission dates based on device selected
        dates['max_day'] = Transmission.objects.filter(device=device)\
                                       .last().timestamp
        dates['min_day'] = Transmission.objects.filter(device=device)\
                                       .first().timestamp

        # Start date is past last transission -> display most recent day data

    form = SelectionForm(initial = {'device': device, 'metric': metric})

    # Get the transimssion data for display from db based on date range
    transmissions = Transmission.objects.filter(device=device,
                                                timestamp__range=
                                                (dates['start_day'],
                                                dates['end_day']))

    # Find the selected device health for display
    device_health = locations[device]['health']

    # Render the html template and pass in the required data
    return render(request, 'index.html', {'form': form,
                                          'locations': locations,
                                          'health': health,
                                          'metric': metric,
                                          'device': device,
                                          'device_health': device_health,
                                          'dates': dates,
                                          'transmissions': transmissions})


def ui(request):
    return render(request, 'ui.html', context=None)
