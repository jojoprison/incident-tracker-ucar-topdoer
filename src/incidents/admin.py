from django.contrib import admin

from .models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("id", "short_text", "status", "source", "created_at")
    list_display_links = ("id", "short_text")
    list_filter = ("status", "source")
    search_fields = ("text",)
    ordering = ("-id",)

    @admin.display(description="Text", ordering="text")
    def short_text(self, obj: Incident) -> str:
        text = obj.text or ""
        return text if len(text) <= 50 else f"{text[:50]}…"
