from project.models import Project ,Task
from users.models import User
from rest_framework import viewsets
from project.api.serializers import  ProjectSerializer ,TaskSerializer
from rest_framework import generics
from rest_framework.response import Response

class AllProjectsView(generics.ListCreateAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

all_projects_page_view = AllProjectsView.as_view()

class AllTasksView(generics.ListCreateAPIView):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

all_tasks_page_view = AllTasksView.as_view()


class ProjectView(generics.ListCreateAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request,project_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Project.objects.filter(id=project_id)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

project_page_view = ProjectView.as_view()


class EmployeeProjectsView(generics.ListCreateAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request,employee_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        user = User.objects.get(id=employee_id)
        queryset = Project.objects.filter(createdby=user.createdby)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

employee_projects_page_view = EmployeeProjectsView.as_view()

class EmployeeProjectView(generics.ListCreateAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request,employee_id,project_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        user = User.objects.get(id=employee_id)
        queryset = Project.objects.filter(createdby=user.createdby,id=project_id)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

employee_project_page_view = EmployeeProjectView.as_view()


class TasksView(generics.ListCreateAPIView):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request,project_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Task.objects.filter(project_id=project_id)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

tasks_page_view = TasksView.as_view()

class TaskView(generics.ListCreateAPIView):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request,project_id,task_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Task.objects.filter(id=task_id,project_id=project_id)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

task_page_view = TaskView.as_view()

