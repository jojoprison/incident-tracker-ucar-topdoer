from typing import Optional

from django.db.models import QuerySet

from .models import Incident, IncidentStatus


def list_incidents(status: Optional[str] = None) -> QuerySet[Incident]:
    qs = Incident.objects.all()

    if status:
        valid = {choice for choice, _ in IncidentStatus.choices}
        if status not in valid:
            raise ValueError(f"Unknown status: {status}")

        qs = qs.filter(status=status)

    return qs
