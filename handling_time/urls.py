from django.urls import path
from .views import AllegroCallbackView, AllegroGetOffersView, HandlingTimeConfigView, HandlingTimeBulkConfigView

urlpatterns = [
    path('api/allegro/callback/', AllegroCallbackView.as_view()),
    path('offers/', AllegroGetOffersView.as_view()),
    path('config/', HandlingTimeConfigView.as_view()),
    path("config/all/", HandlingTimeBulkConfigView.as_view())
]
