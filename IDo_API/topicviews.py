from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Topic, SubTopic
from django.contrib.auth.decorators import login_required
from .serializer import TopicSerializer, SubTopicSerializer

@api_view(['POST'])
@login_required
def create_topic(request):
    owner = request.user.pk
    data = request.data
    data["owner"] = owner
    serializer = TopicSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@login_required
def edit_topic(request, pk):
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        owner = request.user
        data = request.data
        data["owner"] = owner.pk
        serializer = TopicSerializer(topic, data=data)
        if serializer.is_valid():
            if owner == topic.owner:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@login_required
def delete_topic(request, pk):
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        owner = request.user
        if owner == topic.owner:
            topic.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@login_required
def get_topics(request):
    try:
        topic = Topic.objects.filter(owner=request.user)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = TopicSerializer(topic, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@login_required
def get_topic(request, pk):
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        if request.user == topic.owner:
            serializer = TopicSerializer(topic)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@login_required
def create_subtopic(request, pk):
    user = request.user
    data = request.data
    data["topic"] = pk
    serializer = SubTopicSerializer(data=data)
    if serializer.is_valid():
        if Topic.objects.get(pk=pk)["owner"] == user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@login_required
def edit_subtopic(request, pk):
    try:
        subtopic = SubTopic.objects.get(pk=pk)
    except SubTopic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        user = request.user
        data = request.data
        data["topic"] = subtopic.topic
        serializer = TopicSerializer(subtopic, data=data)
        if serializer.is_valid():
            if user == subtopic.topic.owner:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@login_required
def delete_subtopic(request, pk):
    try:
        subtopic = SubTopic.objects.get(pk=pk)
    except SubTopic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        owner = request.user
        if owner == subtopic.topic.owner:
            subtopic.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@login_required
def get_subtopics(request):
    try:
        subtopic = SubTopic.objects.filter(owner=request.user)
    except SubTopic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = TopicSerializer(subtopic, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@login_required
def get_subtopic(request, pk):
    try:
        subtopic = SubTopic.objects.get(pk=pk)
    except SubTopic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        if subtopic.topic.owner == request.user:
            serializer = TopicSerializer(subtopic)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)