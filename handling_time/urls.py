from django.urls import path
from .views import AllegroCallbackView, AllegroGetOffersView, HandlingTimeConfigView

urlpatterns = [
    path('api/allegro/callback/', AllegroCallbackView.as_view()),
    path('offers/', AllegroGetOffersView.as_view()),
    path('config/', HandlingTimeConfigView.as_view())
]
