from django.db import models

# Create your models here.

class Bug(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=5000)
    status = models.CharField(max_length=12, null=True)
    open_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    closed_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str([self.name, self.description, self.status, self.open_time, self.closed_time])