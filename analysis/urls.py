from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SwingViewSet, upload_page, results_page

router = DefaultRouter()
router.register(r'swings', SwingViewSet)

urlpatterns = [
    path('', upload_page, name='home'),
    path('results/<int:swing_id>/', results_page, name='results'),
    path('api/', include(router.urls)),
]
