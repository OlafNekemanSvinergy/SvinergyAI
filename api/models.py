from django.db import models

# Create your models here.
class ApiKey(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    api_key = models.CharField(max_length=30)
