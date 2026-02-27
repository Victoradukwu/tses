from django_filters import rest_framework as filters


class AuditFilter(filters.FilterSet):

    event = filters.CharFilter(lookup_expr='iexact')
    email = filters.CharFilter(lookup_expr='iexact')
    from_ = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    to_ = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')