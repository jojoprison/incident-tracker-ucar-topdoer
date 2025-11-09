from .models import Incident


def create_incident(*, text: str, source: str, status: str | None = None) -> Incident:
    data: dict = {"text": text, "source": source}

    if status is not None:
        data["status"] = status

    return Incident.objects.create(**data)


def update_status(incident: Incident, *, status: str) -> Incident:
    incident.status = status
    incident.save(update_fields=["status"])
    return incident
