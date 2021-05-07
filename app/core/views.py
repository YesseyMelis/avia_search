from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response

from app.core.filters import SearchFilterSet
from app.core.models import City
from app.core.serializers import SearchSerializer


class AirportsSearchViewSet(generics.ListAPIView):
    queryset = City.objects.all().select_related('airports')
    filterset_class = SearchFilterSet
    serializer_class = SearchSerializer
    filter_backends = [DjangoFilterBackend]

    def filter_queryset(self, queryset):
        return super(AirportsSearchViewSet, self).filter_queryset(queryset)

    @method_decorator(cache_page(60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        cities = self.filter_queryset(self.get_queryset()).distinct('code')
        serializer = self.serializer_class(cities, many=True)
        return Response({"cities": serializer.data})
