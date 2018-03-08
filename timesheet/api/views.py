from timesheet.models import TimeSheet
from rest_framework import viewsets
from timesheet.api.serializers import  TimesheetSerializer 
from rest_framework import generics
from rest_framework.response import Response



class EmployeeProjectTimeSheetView(generics.ListCreateAPIView):
    
    queryset = TimeSheet.objects.all()
    serializer_class = TimesheetSerializer

    def get(self, request,employee_id,project_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = TimeSheet.objects.filter(project_id=project_id,employee_id=employee_id)
        serializer = TimesheetSerializer(queryset, many=True)
        return Response(serializer.data)

employee_project_timesheet_page_view = EmployeeProjectTimeSheetView.as_view()

