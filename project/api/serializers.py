from rest_framework import serializers

from project.models import Project ,Task


# serializer class for project model
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'createdby', 'client' )
        # fields = '__all__' 

# serializer class for task model
class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Task
        fields = ('project', 'id' ,'title', 'employee' )

