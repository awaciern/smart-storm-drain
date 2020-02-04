from django.shortcuts import render
from datetime import datetime, timezone, timedelta
from .models import Device, Transmission
from .forms import SelectionForm

def index(request):
    # # Initialize empty date dict
    # dates = {}
    #
    # # If user selects a device/metric/date range, display proper data
    # if request.method == 'POST':
    #     # POST data from python form
    #     metric = request.POST.get('metric')
    #     device = Device.objects.get(pk=request.POST.get('device'))
    #
    #     # POST date data from JS form requiring processing
    #     start_day_raw = request.POST.get('from').split('/')
    #     dates['start_day'] = datetime(int(start_day_raw[2]),
    #                                   int(start_day_raw[0]),
    #                                   int(start_day_raw[1])).astimezone(tz=None)
    #     end_day_raw = request.POST.get('to').split('/')
    #     dates['end_day'] = datetime(int(end_day_raw[2]),
    #                                 int(end_day_raw[0]),
    #                                 int(end_day_raw[1])).astimezone(tz=None)
    #
    #     # Find max and min transmission dates based on device selected
    #     dates['max_day'] = Transmission.objects.filter(device=device)\
    #                                    .last().timestamp.astimezone(tz=None)
    #     dates['min_day'] = Transmission.objects.filter(device=device)\
    #                                    .first().timestamp.astimezone(tz=None)
    #
    #     # Start date is past last transission -> display most recent day data
    #     if dates['start_day'] > dates['max_day']:  # message???
    #        dates['start_day'] = datetime(dates['max_day'].year,
    #                                      dates['max_day'].month,
    #                                      dates['max_day'].day).astimezone(tz=None)
    #        dates['end_day'] = (datetime(dates['max_day'].year,
    #                                     dates['max_day'].month,
    #                                     dates['max_day'].day)
    #                            + timedelta(days=1)).astimezone(tz=None)
    #
    #     # End date is before first transission -> display most recent day data
    #     if dates['end_day'] < dates['min_day']:  # message???
    #        dates['start_day'] = datetime(dates['max_day'].year,
    #                                      dates['max_day'].month,
    #                                      dates['max_day'].day).astimezone(tz=None)
    #        dates['end_day'] = (datetime(dates['max_day'].year,
    #                                     dates['max_day'].month,
    #                                     dates['max_day'].day)
    #                            + timedelta(days=1)).astimezone(tz=None)
    #
    # # User has not submitted data but is visiting page
    # else:
    #     # Initially select water depth of first device in db
    #     metric = 'depth'
    #     device = Device.objects.first()
    #
    #     # Initially set date range of most recent day's data
    #     dates['start_day'] = Transmission.objects.filter(device=device)\
    #                                      .last().timestamp.astimezone(tz=None)
    #     dates['start_day'] = datetime(dates['start_day'].year,
    #                                   dates['start_day'].month,
    #                                   dates['start_day'].day)
    #     dates['end_day'] = dates['start_day']
    #
    #     # Find min transmission dates based on device selected
    #     dates['max_day'] = dates['start_day']
    #     dates['min_day'] = Transmission.objects.filter(device=device)\
    #                                    .first().timestamp.astimezone(tz=None)
    #
    # # Create the python form with the initial values
    # form = SelectionForm(initial = {'device': device, 'metric': metric})
    #
    # # Get the transimssion data for display from db based on date range
    # dt1 = dates['start_day']
    # dt2 = dates['end_day'] + timedelta(days=1)
    # transmissions = Transmission.objects.filter(device=device,
    #                                             timestamp__range=(dt1, dt2))

    ################### NEW #####################
    if request.method == 'POST':
        print(request.POST)

    # Initialize empty date dict
    dates = {}

    # Initially select water depth of first device in db
    metric = 'depth'
    device = Device.objects.first()

    # Initially set date range of most recent day's data
    dates['start_day'] = Transmission.objects.filter(device=device)\
                                     .last().timestamp.astimezone(tz=None)
    dates['start_day'] = datetime(dates['start_day'].year,
                                  dates['start_day'].month,
                                  dates['start_day'].day)
    dates['end_day'] = dates['start_day']

    # Find min transmission dates based on device selected
    dates['max_day'] = dates['start_day']
    dates['min_day'] = Transmission.objects.filter(device=device)\
                                   .first().timestamp.astimezone(tz=None)

    form = SelectionForm(initial = {'device': device, 'metric': metric})

    # Get the transimssion data for display from db based on date range
    dt1 = dates['start_day']
    dt2 = dates['end_day'] + timedelta(days=1)
    transmissions = Transmission.objects.filter(device=device,
                                                timestamp__range=(dt1, dt2))

    # Render the html template and pass in the required data
    return render(request, 'index.html', {'form': form,
                                          'metric': metric,
                                          'device': device,
                                          'dates': dates,
                                          'transmissions': transmissions})


def ui(request):
    return render(request, 'ui.html', context=None)
