from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from project.models import Project ,Task
from project.api.serializers import  ProjectSerializer ,TaskSerializer ,CreateProjectSerializer ,EditProjectSerializer

# view to list all projjects
class AllProjectsView(generics.ListAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request):
        try :
            user = User.objects.get(email=request.user.email)
            if user :
                queryset = Project.objects.filter(createdby= user.id)
                serializer = ProjectSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({'status': False, 'message': 'Authorization required for Project view'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print e
            return Response({'status': False, 'message': 'Authorization required for Project view'}, status=status.HTTP_404_NOT_FOUND)
        


# view to list a project by project id
class ProjectView(generics.ListAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request,project_id):
        try :
            user = User.objects.get(email=request.user.email)
            if user :
                queryset = Project.objects.filter(createdby= user.id,id=project_id)
                serializer = ProjectSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({'status': False, 'message': 'Authorization required for Project view'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print e
            return Response({'status': False, 'message': 'Authorization required for Project view'}, status=status.HTTP_404_NOT_FOUND)
        

# view to list project for employee
class EmployeeProjectsView(generics.ListAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request,employee_id):
        user = User.objects.get(id=employee_id)
        queryset = Project.objects.filter(createdby=user.createdby)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)


# view to list a project by project id for employee by employee id
class EmployeeProjectView(generics.ListAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request,employee_id,project_id):
        user = User.objects.get(id=employee_id)
        queryset = Project.objects.filter(createdby=user.createdby,id=project_id)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)


# view to list tasks for a project by project id
class TasksView(generics.ListAPIView):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request,project_id):
        try :
            user = User.objects.get(email=request.user.email)
            if user.role == 'manager' :
                queryset = Task.objects.filter(project_id=project_id)
                serializer = TaskSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({'status': False, 'message': 'Authorization required for task view'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print e
            return Response({'status': False, 'message': 'Authorization required for task view'}, status=status.HTTP_404_NOT_FOUND)
        


# view to list a task by task id for employees
class TaskView(generics.ListAPIView):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request,project_id,task_id):
        try :
            user = User.objects.get(email=request.user.email)
            if user.role == 'manager' :
                queryset = Task.objects.filter(project_id=project_id,id=task_id)
                serializer = TaskSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({'status': False, 'message': 'Authorization required for task view'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print e
            return Response({'status': False, 'message': 'Authorization required for task view'}, status=status.HTTP_404_NOT_FOUND)


class CreateProjectApiView(generics.CreateAPIView):
    serializer_class = CreateProjectSerializer

    def post(self,request):
        data=request.data
        # import pdb; pdb.set_trace()
        try:
            user = User.objects.get(email=request.user)
            client = User.objects.get(id=data['client'])
            mutable = data._mutable
            data._mutable = True
            data['client'] = client.pk
            data['createdby'] = user.id
            data._mutable = mutable
            project_serializer = CreateProjectSerializer(data=data,context={'request': request})
            if project_serializer.is_valid(raise_exception=True) and user.role == 'manager' :
                project = project_serializer.save()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'status': False,'message':'Authorized Manager Required to Crate a Projet'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            return Response(data, status=status.HTTP_200_OK)
        
   
# view to list all projjects
class EditProjectsApiView(generics.ListAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request):
        user = User.objects.get(email=request.user)
        queryset = Project.objects.filter(createdby= user.id)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

class EditProjectApiView(generics.CreateAPIView):
    
    queryset = Project.objects.all()
    serializer_class = EditProjectSerializer

    def get(self, request, project_id):
        user = User.objects.get(email=request.user)
        queryset = Project.objects.filter(createdby= user.id,id=project_id)
        serializer = EditProjectSerializer(queryset, many=True)
        return Response(serializer.data)
   
    def put(self,request, project_id):
        data=request.data
        # import pdb; pdb.set_trace()
        try:
            user = User.objects.get(email=request.user)
            project = Project.objects.get(id=project_id)
            if data['title']:
                project.title = data['title']
            if data['discription']:
                project.discription = data['discription']
            if data['startdate']:
                project.startdate = data['startdate']
            if data['enddate']:
                project.enddate = data['enddate']
            project.save()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print e
            return Response({'status': False, 'message': 'Can Not Update Project'}, status=status.HTTP_404_NOT_FOUND)

class DeleteProjectsApiView(generics.ListAPIView):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request):
        user = User.objects.get(email=request.user)
        queryset = Project.objects.filter(createdby= user.id)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)


class DeleteProjectApiView(generics.ListAPIView):
    
    queryset = Project.objects.all()
    serializer_class = EditProjectSerializer

    def get(self, request, project_id):
        user = User.objects.get(email=request.user)
        Task.objects.filter(project_id=project_id).delete()
        queryset = Project.objects.filter(createdby= user.id,id=project_id).delete()
        serializer = EditProjectSerializer(queryset, many=True)
        return Response({'status': True, 'message': 'Project and its Tasks  Deleted Successfully'}, status=status.HTTP_200_OK)


