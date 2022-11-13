from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view, 
    permission_classes
)

from .permissions import IsAuthor

from logs.models import (
    Subject,
    Topic,
    Entry
)
from .serializers import (
    SubjectSerializer,
    TopicSerializer,
    EntrySerializer
)


@api_view(['GET', 'POST'])
def subject_list(request, format=None):
    """ List all subjects, or create a new subject """
    if request.method == 'GET':
        subjects = Subject.objects.filter(owner=request.user).order_by('-date_added')
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated,])
def subject_detail(request, slug, format=None):
    """ Retrieve, update or delete a subject """
    subject = get_object_or_404(Subject, owner=request.user, slug=slug)

    if request.method == 'GET':
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def topic_create(request, subject_slug, format=None):
    """ Create a new topic """
    subject = get_object_or_404(Subject, owner=request.user, slug=subject_slug)

    if request.method == 'POST':
        serializer = TopicSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(subject=subject)
            return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicDetail(APIView):
    """ Retrieve, update or delete a topic """

    def get_object(self, request, subject_slug, pk):
        return get_object_or_404(Topic, subject__slug=subject_slug, 
        subject__owner=request.user, pk=pk)

    def get(self, request, subject_slug, pk, format=None):
        topic = self.get_object(request, subject_slug, pk)
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    def put(self, request, subject_slug, pk, format=None):
        topic = self.get_object(request, subject_slug, pk)
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subject_slug, pk, format=None):
        topic = self.get_object(request, subject_slug, pk)
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def entry_create(request, subject_slug, topic_pk):
    topic = get_object_or_404(Topic, subject__slug=subject_slug, 
    subject__owner=request.user, pk=topic_pk)

    if request.method == 'POST':
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(topic=topic)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)

class EntryDetail(APIView):
    """" Update and delete an entry """

    def get_object(self, request, subject_slug, topic_pk, pk):
        return get_object_or_404(Entry, topic__subject__slug=subject_slug,
        topic__subject__owner=request.user, topic__pk=topic_pk, pk=pk)

    def put(self, request, subject_slug, topic_pk, pk):
        entry = self.get_object(request, subject_slug, topic_pk, pk)
        serializer = EntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subject_slug, topic_pk, pk):
        entry = self.get_object(request, subject_slug, topic_pk, pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)