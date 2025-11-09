from rest_framework import serializers

from .models import Incident, IncidentSource, IncidentStatus


class IncidentCreateSerializer(serializers.Serializer):
    text = serializers.CharField(allow_blank=False)
    source = serializers.ChoiceField(choices=IncidentSource.choices)
    status = serializers.ChoiceField(choices=IncidentStatus.choices, required=False)


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ["id", "text", "status", "source", "created_at"]


class StatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=IncidentStatus.choices)
