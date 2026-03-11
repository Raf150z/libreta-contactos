from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'contactos', views.ContactoViewSet, basename='api-contacto')

urlpatterns = [
    path('', include(router.urls)),
]