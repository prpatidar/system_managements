from timesheet.models import TimeSheet
from rest_framework import serializers

# sereializer class for timesheet model
class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        fields = '__all__' 
