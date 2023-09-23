from rest_framework import routers
from .views import ProductStatsModelViewSet, ProductViewSet, LessonViewSet

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'lesson', LessonViewSet, basename='lesson')
router.register(r'statistics', ProductStatsModelViewSet, basename='statistics')
urlpatterns = router.urls
