from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Incident
from .selectors import list_incidents
from .serializers import (
    IncidentCreateSerializer,
    IncidentSerializer,
    StatusUpdateSerializer,
)
from .services import create_incident, update_status


class IncidentViewSet(viewsets.GenericViewSet):
    queryset = Incident.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return IncidentCreateSerializer
        if self.action == "status":
            return StatusUpdateSerializer
        return IncidentSerializer

    def list(self, request):

        status_param = request.query_params.get("status")

        try:
            qs = list_incidents(status_param)
        except ValueError as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = IncidentSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):

        serializer = IncidentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        incident = create_incident(**serializer.validated_data)

        return Response(
            IncidentSerializer(incident).data, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["patch"], url_path="status")
    def status(self, request, pk=None):

        instance = get_object_or_404(Incident, pk=pk)

        serializer = StatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        update_status(instance, status=serializer.validated_data["status"])

        return Response(IncidentSerializer(instance).data)
