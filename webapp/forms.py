from django import forms
from .models import Device


class SelectionForm(forms.ModelForm):
    # Dropdown menu listing devices
    device = forms.ModelChoiceField(queryset=Device.objects.all(),
                                    empty_label=None)

    # Select button for display metrics
    METRICS = [('depth', 'Water Depth'),
               ('flowrate', 'Flow Rate'),
               ('voltage', 'Battery Voltage')]
    metric = forms.ChoiceField(choices=METRICS, widget=forms.Select)


    class Meta:
        model = Device
        fields = ()
