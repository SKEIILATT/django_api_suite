from django.urls import path
from .views import LandingAPI

urlpatterns = [
    # Asociamos la ruta "index/" a la vista LandingAPI
     path("index/", LandingAPI.as_view(), name="index"),
]
