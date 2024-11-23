from rest_framework.routers import DefaultRouter

from .views import AuthUserViewSet

router = DefaultRouter()
router.register('auth', AuthUserViewSet, basename='auth')

urlpatterns = router.urls
