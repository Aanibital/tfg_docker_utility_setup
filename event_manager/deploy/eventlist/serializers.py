from .models import EventList, Event
from rest_framework import serializers


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventList
        fields = ['name', 'users']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'event_list', 'description', 'completed', 'notes']