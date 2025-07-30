from django.urls import path, include
from . import views

urlpatterns = [
    path("index/", views.DemoRestApi.as_view(), name="demo_rest_api_resources"),
    path("<str:item_id>/", views.DemoRestApiItem.as_view(), name="demo_rest_api_item"),
    path("landing/api/", include("landing_api.urls")),
]