from django import forms
from .models import Device

# class MessageForm(forms.ModelForm):
#
#     class Meta:
#         model = Message
#         fields = ('text',)


class DeviceForm(forms.ModelForm):
    device = forms.ModelChoiceField(queryset=Device.objects.all(),
                                    empty_label=None)

    class Meta:
        model = Device
        fields = ()
