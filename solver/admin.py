from django.contrib import admin
from .models import Solver


@admin.register(Solver)
class SolverAdmin(admin.ModelAdmin):
    search_fields = ['user.email', 'status', 'task_id']

