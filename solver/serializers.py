from rest_framework import serializers
from .models import Solver


class SolverSerializer(serializers.ModelSerializer):
    """Serializer to Solver model."""
    coefficients = serializers.ListField(
        child=serializers.ListField(child=serializers.FloatField()),
        required=True
    )
    constants = serializers.ListField(
        child=serializers.FloatField(),
        required=True
    )

    class Meta:
        model = Solver
        fields = ['id', 'user', 'coefficients', 'constants', 'result', 'status', 'progress', 'created_at', 'updated_at']
        read_only_fields = ['user', 'result', 'status', 'progress', 'created_at', 'updated_at']
