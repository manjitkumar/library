
from rest_framework import viewsets

from libs.pagination import ResultSetPagination

from publishers.models import Publisher
from publishers.serializers import PublisherSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    pagination_class = ResultSetPagination
