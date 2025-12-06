from django.db import models

class Swing(models.Model):
    video = models.FileField(upload_to='swings/')
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    analysis_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Swing {self.id} - {self.created_at}"
