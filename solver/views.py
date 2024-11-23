from rest_framework.viewsets import ModelViewSet
from .serializers import SolverSerializer
from rest_framework.response import Response
from celery.result import AsyncResult
from django.shortcuts import get_object_or_404
from .models import Solver
from .tasks import solve_system
from rest_framework.decorators import action


class SolverViewSet(ModelViewSet):
    queryset = Solver.objects.all()
    serializer_class = SolverSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Override the creation to run the Celery task after saving the object.
        """
        solver = serializer.save(user=self.request.user)
        task = solve_system.apply_async((solver.coefficients, solver.constants))
        solver.status = 'PROCESSING'
        solver.save(update_fields=['status'])

        solver.task_id = str(task.id)
        solver.save(update_fields=['task_id'])

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """
        An additional method for checking the progress of a task.
        """
        solver = get_object_or_404(Solver, pk=pk)
        task_id = solver.task_id

        if not task_id:
            return Response({'error': 'Task ID not found'}, status=400)

        task_result = AsyncResult(task_id)
        print(task_result.state)

        if task_result.state == 'PROGRESS':
            progress = task_result.info.get('current', 0) * 100 // task_result.info.get('total', 1)
            solver.progress = progress
            solver.save(update_fields=['progress'])
            return Response({'state': task_result.state, 'progress': progress})

        elif task_result.state == 'SUCCESS':
            solver.status = 'COMPLETED'

            result = task_result.result
            if isinstance(result, dict):
                result = f"{result.get('status')}: {result.get('message')}"

            solver.result = result
            solver.save(update_fields=['status', 'result'])

            return Response({'state': task_result.state, 'result': result})

        elif task_result.state == 'FAILURE':
            solver.status = 'FAILURE'
            solver.result = 'FAILURE'
            solver.save(update_fields=['status', 'result'])
            return Response({'state': task_result.state, 'result': f"{task_result.info.get('status')}: {task_result.info.get('message')}"})

        return Response({'state': task_result.state})