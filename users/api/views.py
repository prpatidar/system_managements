from rest_framework import generics ,viewsets
from rest_framework.response import Response

from users.models import User
from users.api.serializers import UserSerializer
from users.api.permissions import IsOwnerOrReadOnly


# class UserMixin(object):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsOwnerOrReadOnly,)

#     def pre_save(self,obj):
#         obj.owner = self.request.user


# view for allmanagers in application
class AllManagersView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(role="manager")
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# view for all employees
class AllEmployeesView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(role="employee")
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# view to list all clients
class AllClientsView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(role="client")
    serializer_class = UserSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# view to list a particular employee by its id
class EmployeeView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(role="employee")
    serializer_class = UserSerializer

    def get(self, request,employee_id):
        queryset = User.objects.filter(role="employee",id=employee_id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# view to list particular client by its unique id
class ClientView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(role="client")
    serializer_class = UserSerializer

    def get(self, request,client_id):
        queryset = User.objects.filter(role="client",id=client_id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)