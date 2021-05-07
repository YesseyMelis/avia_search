from django.urls import path

from app.core.views import AirportsSearchViewSet

urlpatterns = [
    path('search/', AirportsSearchViewSet.as_view(), name='search-city-airport'),
]
