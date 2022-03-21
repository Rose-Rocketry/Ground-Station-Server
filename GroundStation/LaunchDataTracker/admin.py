from django.contrib import admin
from .models import *

# Register your models here.
#class LaunchAdmin(admin.ModelAdmin):
#    pass

admin.site.register(LaunchInfo)
admin.site.register(TelemetryPacket)