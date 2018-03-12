from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from timesheet.models import TimeSheet
from timesheet.api.serializers import  TimesheetSerializer 

# view to list all timesheet for employee by employee id and project id
class EmployeeProjectTimeSheetView(generics.ListCreateAPIView):
    
    queryset = TimeSheet.objects.all()
    serializer_class = TimesheetSerializer

    def get(self, request,employee_id,project_id):
        queryset = TimeSheet.objects.filter(project_id=project_id,employee_id=employee_id)
        serializer = TimesheetSerializer(queryset, many=True)
        return Response(serializer.data)


