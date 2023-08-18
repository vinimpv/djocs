from .views import index
from django.urls import path
from django.urls import include


urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("allauth.urls")),
]
