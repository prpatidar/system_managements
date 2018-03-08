from users.models import User
from rest_framework import viewsets
from users.api.serializers import UserSerializer
from rest_framework import generics
from rest_framework.response import Response



class AllManagersView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(role="manager")
    serializer_class = UserSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

managers_page_view = AllManagersView.as_view()

class AllEmployeesView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(role="employee")
    serializer_class = UserSerializer

    def get(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

all_employees_page_view = AllEmployeesView.as_view()

class AllClientsView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(role="client")
    serializer_class = UserSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

clients_page_view = AllClientsView.as_view()


class EmployeeView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(role="employee")
    serializer_class = UserSerializer

    def get(self, request,employee_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = User.objects.filter(role="employee",id=employee_id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

employee_page_view = EmployeeView.as_view()

class ClientView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(role="client")
    serializer_class = UserSerializer

    def get(self, request,client_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = User.objects.filter(role="client",id=client_id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

client_page_view = ClientView.as_view()
