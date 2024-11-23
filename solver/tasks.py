import numpy as np

from django.conf import settings

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded


@shared_task(bind=True, time_limit=settings.SOLVER_TASK_TIME_LIMIT)
def solve_system(self, coefficients, constants):
    try:
        total_steps = len(coefficients)
        for i in range(total_steps):
            self.update_state(state='progress', meta={'current': i + 1, 'total': total_steps})

        A = np.array(coefficients)
        B = np.array(constants)
        solution = np.linalg.solve(A, B)

        self.update_state(state='SUCCESS', meta=solution.tolist())
        return {'status': 'success', 'solution': solution.tolist()}

    except np.linalg.LinAlgError as e:
        self.update_state(state='FAILURE')
        return {'status': 'error', 'message': str(e)}
    except SoftTimeLimitExceeded:
        self.update_state(state='FAILURE')
        return {'status': 'error', 'message': 'Time limit exceeded'}
