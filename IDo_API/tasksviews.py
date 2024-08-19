from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task, SubTopic
from django.contrib.auth.decorators import login_required
from .serializer import TasksSerializer

@api_view(['POST'])
@login_required
def create_task(request, pk):
    data = request.data
    user = request.user
    try:
        data["subtopic"] = pk
        SubTopic.objects.get(pk=pk)
    except SubTopic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TasksSerializer(data=data)
    if serializer.is_valid():
        if SubTopic.objects.get(pk=pk).topic.owner == user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@login_required
def edit_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        user = request.user
        data = request.data
        data["subtopic"] = task.subtopic
        serializer = TasksSerializer(task, data=data)
        if serializer.is_valid():
            if user == task.subtopic.topic.owner:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@login_required
def delete_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        owner = request.user
        if owner == task.subtopic.topic.owner:
            task.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@login_required
def get_tasks(request):
    try:
        tasks = Task.objects.filter(owner=request.user)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@login_required
def get_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        if task.subtopic.topic.owner == request.user:
            serializer = TasksSerializer(task)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)