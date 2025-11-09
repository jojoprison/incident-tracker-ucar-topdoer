from django.db import models


class IncidentStatus(models.TextChoices):
    NEW = "new", "New"
    INVESTIGATING = "investigating", "Investigating"
    RESOLVED = "resolved", "Resolved"
    CANCELLED = "cancelled", "Cancelled"


class IncidentSource(models.TextChoices):
    OPERATOR = "operator", "Operator"
    MONITORING = "monitoring", "Monitoring"
    PARTNER = "partner", "Partner"


class Incident(models.Model):
    text = models.TextField()
    status = models.CharField(
        max_length=32,
        choices=IncidentStatus.choices,
        default=IncidentStatus.NEW,
        db_index=True,
    )
    source = models.CharField(
        max_length=32,
        choices=IncidentSource.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"Incident#{self.pk} {self.status}"
