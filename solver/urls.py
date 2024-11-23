from rest_framework.routers import DefaultRouter
from .views import SolverViewSet

router = DefaultRouter()
router.register('', SolverViewSet)

urlpatterns = router.urls
