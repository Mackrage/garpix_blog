import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from blog.models import BlogPage
from blog.serializers import BlogPageSerializer, BlogPageListSerializer
from rest_framework.permissions import BasePermission


class BlogPagePagination(PageNumberPagination):

    def get_page_size(self, request):
        page_size = request.GET.get('page_size', 10)
        return page_size


class BlogPageFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active', )
    created_at = django_filters.DateTimeFilter(field_name="created_at",
                                               lookup_expr='gte')

    class Meta:
        model = BlogPage
        fields = ['created_at', 'type', 'category']


class BlogPageViewSet(ModelViewSet):
    queryset = BlogPage.objects.all()
    permission_classes = [BasePermission, ]
    pagination_class = BlogPagePagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = BlogPageFilter
    ordering_fields = ['updated_at', ]

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPageListSerializer
        return BlogPageSerializer
