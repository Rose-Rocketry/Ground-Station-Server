from django.contrib import admin
from django import forms
from .models import *

# Register your models here.
class LaunchAdminForm(forms.ModelForm):
    """Form Validation for adding Launches"""

    def clean(self):
        print("CLEANS =======")
        cleaned_data = super().clean()
        active = cleaned_data.get("launch_active")
        computer = cleaned_data.get("flight_computer")
        number_active = LaunchInfo.objects.filter(active_launch = True, flight_computer = computer)
        print(f"{number_active}===========")
        if(len(number_active) > 0):
            print("Raised")
            raise forms.ValidationError(f"There is already a launch with {computer} as the active flight computer.")

@admin.register(LaunchInfo)
class LaunchAdmin(admin.ModelAdmin):
    """Admin Page Settings for Launches"""
    form = LaunchAdminForm


admin.site.register(TelemetryPacket)
admin.site.register(Payload)