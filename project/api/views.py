from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from users.models import User
from project.models import Project ,Task
from project.api.serializers import  ProjectSerializer ,TaskSerializer

# view to list all projjects
class AllProjectsView(generics.ListCreateAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)


# view to list all tasks 
class AllTasksView(generics.ListCreateAPIView):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)


# view to list a project by project id
class ProjectView(generics.ListCreateAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request,project_id):
        queryset = Project.objects.filter(id=project_id)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)


# view to list project for employee
class EmployeeProjectsView(generics.ListCreateAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request,employee_id):
        user = User.objects.get(id=employee_id)
        queryset = Project.objects.filter(createdby=user.createdby)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)


# view to list a project by project id for employee by employee id
class EmployeeProjectView(generics.ListCreateAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request,employee_id,project_id):
        user = User.objects.get(id=employee_id)
        queryset = Project.objects.filter(createdby=user.createdby,id=project_id)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)


# view to list tasks for a project by project id
class TasksView(generics.ListCreateAPIView):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request,project_id):
        queryset = Task.objects.filter(project_id=project_id)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)


# view to list a task by task id for employees
class TaskView(generics.ListCreateAPIView):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request,project_id,task_id):
        queryset = Task.objects.filter(id=task_id,project_id=project_id)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)