from django.forms import ModelForm
from django import forms
from .models import SystemSettings
import datetime

class SystemSettingsForm(ModelForm):

    
    #DateTime_updated = forms.DateField(
    #   label = 'Date Time Uploaded',
    #    widget = forms.SelectDateWidget(years = range(1992, datetime.date.today().year+1))
    #)   
    
   

    def __init__(self, *args, **kwargs):
        super(SystemSettingsForm, self).__init__(*args, **kwargs)
    
        for name_field in self.fields.keys():
            self.fields[name_field].widget.attrs.update({
                'class':'form-control',
            })
    

    class Meta:
        model = SystemSettings
        fields = ('system_label','system_name','system_value')