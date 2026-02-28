import math

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.audit.filters import AuditFilter
from apps.audit.serializers import AuditSerializer

from .docs import LIST_LOGS
from .models import Audit


class PageSizeAndNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        effective_page_size = int(self.request.query_params.get("page_size", self.page_size))
        page_resp = super().get_paginated_response(data)
        page_obj = page_resp.data
        num_of_pages = math.ceil(page_obj["count"] / effective_page_size)  # type: ignore
        resp_dct = {"number_of_pages": num_of_pages}
        resp_dct.update(page_obj)  # type: ignore
        return Response(resp_dct)


@extend_schema(**LIST_LOGS)
class AuditListView(generics.ListAPIView):
    serializer_class = AuditSerializer
    pagination_class = PageSizeAndNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuditFilter
    search_fields = ["email"]
    ordering_fields = ["id", "event", "email", "ip_address", "user_agent", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):  # type: ignore
        return Audit.objects.all()
