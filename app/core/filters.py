from django.db.models import Q
from django_filters import FilterSet, filters

from app.core.models import City


class SearchFilterField(filters.CharFilter):
    def filter(self, qs, value):
        if value in [None, '', [], {}]:
            return qs
        if self.distinct:
            qs = qs.distinct()
        lookups = (
            '%s__%s' % (self.field_name, lookup_expr)
            for lookup_expr in ('search', 'contains', 'icontains')
        )
        qs_lookup_expression = Q()
        for lookup in lookups:
            qs_lookup_expression |= Q(**{lookup: value})
        qs = self.get_method(qs)(qs_lookup_expression)
        return qs


class SearchFilterSet(FilterSet):
    code = filters.CharFilter(label='Город', method='get_city_air_from_code')

    class Meta:
        model = City
        fields = ('code',)

    def get_city_air_from_code(self, queryset, name, value):
        return City.objects.filter(
            Q(code__icontains=value) |
            Q(name__icontains=value) |
            Q(airports__code__icontains=value) |
            Q(airports__name__icontains=value)
        )
