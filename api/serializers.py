from rest_framework import serializers

from logs.models import (
    Subject,
    Topic,
    Entry
)

class EntrySerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField()

    class Meta:
        model = Entry
        fields = ['id', 'topic', 'text', 'date_added']


class TopicSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    entries = EntrySerializer(read_only=True, many=True)

    class Meta:
        model = Topic
        depth = 1
        fields = ['id', 'topic', 'subject', 'entries', 'date_added']


class SubjectSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'detail', 'owner', 'date_added']