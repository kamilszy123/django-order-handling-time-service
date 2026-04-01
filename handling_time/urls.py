from django.urls import path
from .views import AllegroCallbackView

urlpatterns = [
    path('api/allegro/callback/', AllegroCallbackView.as_view())
]

