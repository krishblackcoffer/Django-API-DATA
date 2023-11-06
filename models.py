from django.db import models

# Create your models here.
class ApiResponse(models.Model):
    response_data = models.JSONField()