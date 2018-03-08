from project.models import Project ,Task
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'createdby', 'client' )
        # fields = '__all__' 

class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Task
        fields = ('project', 'id' ,'title', 'employee' )

