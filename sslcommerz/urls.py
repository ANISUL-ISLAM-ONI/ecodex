from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    InitView,
)


app_name = "sslcommerz"

urlpatterns = [
    path("init", csrf_exempt(InitView.as_view()), name="init"),
]
