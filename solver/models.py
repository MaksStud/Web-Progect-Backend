from django.db import models
from django.conf import settings


class Solver(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solvers')
    coefficients = models.JSONField(default=list)
    constants = models.JSONField(default=list)
    result = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING')
    progress = models.PositiveIntegerField(default=0)
    task_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Solver Task {self.id} for User {self.user.username}"

