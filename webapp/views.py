from django.shortcuts import render
from datetime import datetime, timedelta
from pytz import timezone
from .models import Device, Transmission
from .forms import SelectionForm

def index(request):
    # Create geological locations dict and health dict
    locations = {}
    health = {}

    # Initialize health dict counters
    health['overall'] = 2
    health['healthy'] = 0
    health['flowing'] = 0
    health['flooded'] = 0
    health['offline'] = 0

    for loc in Device.objects.all():
        loc_health = 0  # default health: healthy

        # If the device has no transmissions, it is offline
        if len(Transmission.objects.filter(device=loc)) == 0:
            loc_health = 4  # offline, never been online

        # Eventually, there will be logic here to determine health from metrics
        # Right now, I am just assigning them
        if loc.pk == 1:
            loc_health = 0  # healthy
            health['healthy'] += 1
        elif loc.pk == 2:
            loc_health = 1  # collecting water
            health['flowing'] += 1
        elif loc.pk == 3:
            loc_health = 3  # offline, but has been online before
            health['offline'] += 1
        elif loc.pk == 4:
            loc_health = 4  # offline, has never been online before
            health['offline'] += 1
        elif loc.pk == 5:
            loc_health = 2  # flooded
            health['flooded'] += 1

        # Assign values to dict
        locations[loc] = {'latitude': loc.latitude, 'longitude': loc.longitude,
                          'health': loc_health}

    # Initialize empty date dict
    dates = {}

    # If user selects a device/metric/date range, display proper data
    if request.method == 'POST':
        # POST data from python form
        metric = request.POST.get('metric')
        device = Device.objects.get(pk=request.POST.get('device'))

        # Find the selected device health for display
        device_health = locations[device]['health']

        # If the device has never been online, no need to gather date info
        if device_health != 4:
            # If there is date data from user input
            if request.POST.get('datetimes'):
                # POST date data from JS form requiring processing
                date_list_raw = request.POST.get('datetimes').split('-')
                dates['start_day'] = datetime.strptime(date_list_raw[0],
                                                       '%m/%d/%y %I:%M %p ')\
                                             .replace(tzinfo=timezone('UTC'))\
                                             + timedelta(hours=5)
                dates['end_day'] = datetime.strptime(date_list_raw[1],
                                                     ' %m/%d/%y %I:%M %p')\
                                           .replace(tzinfo=timezone('UTC'))\
                                           + timedelta(hours=5)

                # Find max and min transmission dates based on device selected
                dates['max_day'] = Transmission.objects.filter(device=device)\
                                               .last().timestamp
                dates['min_day'] = Transmission.objects.filter(device=device)\
                                               .first().timestamp

                # Start date is past last transission -> display most recent day data
                if dates['start_day'] > dates['max_day']:  # message???
                    dates['end_day'] = Transmission.objects.filter(device=device)\
                                                           .last().timestamp
                    eastern_date = dates['end_day'] - timedelta(hours=5)
                    dates['start_day'] = datetime(eastern_date.year,
                                                  eastern_date.month,
                                                  eastern_date.day,
                                                  tzinfo=timezone('UTC'))\
                                                  + timedelta(hours=5)

                # End date is before first transission -> display most recent day data
                if dates['end_day'] < dates['min_day']:  # message???
                    dates['end_day'] = Transmission.objects.filter(device=device)\
                                                           .last().timestamp
                    eastern_date = dates['end_day'] - timedelta(hours=5)
                    dates['start_day'] = datetime(eastern_date.year,
                                                  eastern_date.month,
                                                  eastern_date.day,
                                                  tzinfo=timezone('UTC'))\
                                                  + timedelta(hours=5)

            # If there is NOT date data from user input
            else:
                # Initially set date range of most recent day's data
                dates['end_day'] = Transmission.objects.filter(device=device).last()\
                                                       .timestamp
                eastern_date = dates['end_day'] - timedelta(hours=5)
                dates['start_day'] = datetime(eastern_date.year,
                                              eastern_date.month,
                                              eastern_date.day,
                                              tzinfo=timezone('UTC'))\
                                              + timedelta(hours=5)
                # Find min transmission dates based on device selected
                dates['max_day'] = Transmission.objects.filter(device=device)\
                                               .last().timestamp
                dates['min_day'] = Transmission.objects.filter(device=device)\
                                               .first().timestamp

    # User has not yet submitted data; is initially visiting the page
    else:
        # Initially select water depth of first device in db
        metric = 'depth'
        device = Device.objects.first()

        # Find the selected device health for display
        device_health = locations[device]['health']

        # If the device has never been online, no need to gather date info
        if device_health != 4:
            # Initially set date range of most recent day's data
            dates['end_day'] = Transmission.objects.filter(device=device).last()\
                                                   .timestamp
            eastern_date = dates['end_day'] - timedelta(hours=5)
            dates['start_day'] = datetime(eastern_date.year,
                                          eastern_date.month,
                                          eastern_date.day,
                                          tzinfo=timezone('UTC'))\
                                          + timedelta(hours=5)
            # Find min transmission dates based on device selected
            dates['max_day'] = Transmission.objects.filter(device=device)\
                                           .last().timestamp
            dates['min_day'] = Transmission.objects.filter(device=device)\
                                           .first().timestamp

    # Create the form the user will see
    form = SelectionForm(initial = {'device': device, 'metric': metric})

    # Get the transimssion (if any) data for display from db based on date range
    if device_health != 4:
        transmissions = Transmission.objects.filter(device=device,
                                                timestamp__range=
                                                (dates['start_day'],
                                                dates['end_day']))
    else:
        transmissions = []

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
