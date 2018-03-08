from timesheet.models import TimeSheet
from rest_framework import serializers


class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        # fields = ('id', 'title', 'createdby', 'client' )
        fields = '__all__' 
