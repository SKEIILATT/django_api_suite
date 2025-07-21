from django.urls import path
from . import views

urlpatterns = [
   path("", views.index, name="index"),  # URL raíz
   path("index/", views.index, name="index_alt"),  # URL alternativa
]