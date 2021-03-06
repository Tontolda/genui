from genui.accounts.serializers import FilterToUserMixIn
from genui.maps.genuimodels.builders import MapBuilder
from genui.models.genuimodels.bases import Algorithm
from genui.models.views import ModelViewSet, AlgorithmViewSet, FilterToModelMixin
from . import models, serializers, tasks
from rest_framework import generics
from genui.utils.pagination import GenuiPagination


class MapViewSet(ModelViewSet):
    queryset = models.Map.objects.order_by('-created')
    serializer_class = serializers.MapSerializer
    init_serializer_class = serializers.MapInitSerializer
    builder_class = MapBuilder
    build_task = tasks.createMap

class MappingAlgViewSet(AlgorithmViewSet):

    def get_queryset(self):
        current = super().get_queryset()
        return current.filter(validModes__name__in=(Algorithm.MAP,)).distinct('id')

class PointPagination(GenuiPagination):
    page_size = 250

class PointsView(
    FilterToModelMixin,
    FilterToUserMixIn,
    generics.ListAPIView
):
    queryset = models.Point.objects.order_by('id')
    serializer_class = serializers.PointSerializer
    pagination_class = PointPagination
    lookup_field = "map"
    owner_relation = "map__project__owner"