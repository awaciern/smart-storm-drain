from django.shortcuts import render
from datetime import datetime, timedelta
from pytz import timezone
from .models import Device, Transmission, GatewayLog
from .forms import SelectionForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.conf import settings
import json
from urllib.parse import unquote

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
                                               .order_by('-timestamp')[0]\
                                               .timestamp
                dates['min_day'] = Transmission.objects.filter(device=device)\
                                               .order_by('timestamp')[0]\
                                               .timestamp

                # Start date is past last transission -> display most recent day data
                if dates['start_day'] > dates['max_day']:  # message???
                    dates['end_day'] = Transmission.objects\
                                                   .filter(device=device)\
                                                   .order_by('-timestamp')[0]\
                                                   .timestamp
                    eastern_date = dates['end_day'] - timedelta(hours=5)
                    dates['start_day'] = datetime(eastern_date.year,
                                                  eastern_date.month,
                                                  eastern_date.day,
                                                  tzinfo=timezone('UTC'))\
                                                  + timedelta(hours=5)

                # End date is before first transission -> display most recent day data
                if dates['end_day'] < dates['min_day']:  # message???
                    dates['end_day'] = Transmission.objects\
                                                   .filter(device=device)\
                                                   .order_by('-timestamp')[0]\
                                                   .timestamp
                    eastern_date = dates['end_day'] - timedelta(hours=5)
                    dates['start_day'] = datetime(eastern_date.year,
                                                  eastern_date.month,
                                                  eastern_date.day,
                                                  tzinfo=timezone('UTC'))\
                                                  + timedelta(hours=5)

            # If there is NOT date data from user input
            else:
                # Initially set date range of most recent day's data
                dates['end_day'] = Transmission.objects.filter(device=device)\
                                               .order_by('-timestamp')[0]\
                                               .timestamp
                eastern_date = dates['end_day'] - timedelta(hours=5)
                dates['start_day'] = datetime(eastern_date.year,
                                              eastern_date.month,
                                              eastern_date.day,
                                              tzinfo=timezone('UTC'))\
                                              + timedelta(hours=5)
                # Find min transmission dates based on device selected
                dates['max_day'] = Transmission.objects.filter(device=device)\
                                               .order_by('-timestamp')[0]\
                                               .timestamp
                dates['min_day'] = Transmission.objects.filter(device=device)\
                                               .order_by('timestamp')[0]\
                                               .timestamp

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
            dates['end_day'] = Transmission.objects.filter(device=device)\
                                                   .last().timestamp
            eastern_date = dates['end_day'] - timedelta(hours=5)
            dates['start_day'] = datetime(eastern_date.year,
                                          eastern_date.month,
                                          eastern_date.day,
                                          tzinfo=timezone('UTC'))\
                                          + timedelta(hours=5)

            # Find min transmission dates based on device selected
            dates['max_day'] = Transmission.objects.filter(device=device)\
                                           .order_by('-timestamp')[0].timestamp
            dates['min_day'] = Transmission.objects.filter(device=device)\
                                           .order_by('timestamp')[0].timestamp

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
    print(dates)
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


@csrf_exempt
def gateway(request):
    # This URL will be hit with POST data from the gateway and store it in db
    if request.method == 'POST':
        # For logging and debugging the gateway
        raw_data = unquote(request.body.decode('utf-8'))
        #raw_data = raw_data.replace('+', '').replace('request=', '')
        print(raw_data)
        log = GatewayLog.objects.create(raw_data=raw_data, message='EXCEPTION THROWN!')

        # Convert the POST data into a python dictionary
        # req_dict = json.loads(request.POST.get('request'))
        req_dict = json.loads(raw_data)
        log.message = 'req_dict\n' + req_dict + '\n\nraw_data\n' + raw_data
        log.save()
        # print(req_dict['metadata']['time'])

        # return HttpResponse()

        # Check the downlink_url for the "password"
        if 'downlink_url' not in req_dict:
            # GatewayLog.objects.create(raw_data=raw_data, message='Authentication Failure')
            log.message = 'Authentication Failure'
            log.save()
            return HttpResponseForbidden('Authentication Failure')
        if req_dict['downlink_url'] == settings.DL_URL_PW:
            # Get the device id if available
            if 'dev_id' not in req_dict:
                # GatewayLog.objects.create(raw_data=raw_data, message='ERROR: No device identified!')
                log.message = 'ERROR: No device identified!'
                log.save()
                return HttpResponse('ERROR: No device identified!')

            # Check if the device id matches a device in the db
            device_list = []
            for device in Device.objects.all():
                device_list.append(device.name)
            if req_dict['dev_id'] in device_list:
                # Get the device from the database
                device = Device.objects.get(name=req_dict['dev_id'])

                # Check if the POST data has needed payload fields
                if 'payload_fields' not in req_dict:
                    # GatewayLog.objects.create(raw_data=raw_data, message='ERROR: Data has no payload fields!')
                    log.message = 'ERROR: Data has no payload fields!'
                    log.save()
                    return HttpResponse('ERROR: Data has no payload fields!')
                payload_dict = req_dict['payload_fields']
                if 'distance_inches' not in payload_dict or 'luminosity' not in payload_dict:
                    # GatewayLog.objects.create(raw_data=raw_data, message='ERROR: Data lacks needed payload fields!')
                    log.message = 'ERROR: Data lacks needed payload fields!'
                    log.save()
                    return HttpResponse('ERROR: Data lacks needed payload fields!')

                # Check if the POST data has needed metadata
                if 'metadata' not in req_dict:
                    # GatewayLog.objects.create(raw_data=raw_data, message='ERROR: Data has no metadata!')
                    log.message = 'ERROR: Data has no metadata!'
                    log.save()
                    return HttpResponse('ERROR: Data has no metadata!')
                metadata_dict = req_dict['metadata']
                if 'time' not in metadata_dict:
                    # GatewayLog.objects.create(raw_data=raw_data, message='ERROR: Data lacks needed metadata!')
                    log.message = 'ERROR: Data lacks needed metadata!'
                    log.save()
                    return HttpResponse('ERROR: Data lacks needed metadata!')

                print(metadata_dict['time'])

                # POST data is good -> store transission in db
                Transmission.objects.create(timestamp=metadata_dict['time'],
                                            device=device,
                                            depth=payload_dict['distance_inches'],
                                            flowrate=0,
                                            voltage=payload_dict['luminosity'])

                # Return success message
                # GatewayLog.objects.create(raw_data=raw_data, message='SUCCESS: Transmission recieved and stored')
                log.message = 'SUCCESS: Transmission recieved and stored'
                log.save()
                return HttpResponse('SUCCESS: Transmission recieved and stored')
            # If no device match stop and return error message
            else:
                # GatewayLog.objects.create(raw_data=raw_data, message='ERROR: Device ID is not recognized!')
                log.message = 'ERROR: Device ID is not recognized!'
                log.save()
                return HttpResponse('ERROR: Device ID is not recognized!')
        else:
            # GatewayLog.objects.create(raw_data=raw_data, message='Authentication Failure')
            log.message = 'Authentication Failure'
            log.save()
            return HttpResponseForbidden('Authentication Failure')

    # Only POST methods can hit this URL
    else:
        return HttpResponseNotFound()
