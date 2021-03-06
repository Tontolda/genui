"""
urls

Created by: Martin Sicho
On: 25-02-20, 16:29
"""
from django.urls import path, include
from rest_framework import routers

from .models import Map
from . import views
from genui.utils.extensions.tasks.views import ModelTasksView
from genui.models.views import ModelFileView
from genui.qsar.views import DescriptorGroupsViewSet
from .apps import MapsConfig
from genui.utils.inspection import discover_extensions_urlpatterns

router = routers.DefaultRouter()
router.register(r'algorithms',views.MappingAlgViewSet, basename='mapping-algorithm')
router.register(r'descriptors', DescriptorGroupsViewSet, basename='descriptor')
router.register(r'', views.MapViewSet, basename='map')


routes = [
    path('<int:pk>/tasks/all/', ModelTasksView.as_view(model_class=Map))
    , path('<int:pk>/tasks/started/', ModelTasksView.as_view(started_only=True, model_class=Map))
    , path('<int:pk>/files/', ModelFileView.as_view(model_class=Map), name="map-files-list")
    , path('<int:pk>/points/', views.PointsView.as_view(model_class=Map), name="map-points-list")
]

urlpatterns = [
    path('', include(routes)),
    path('', include(router.urls)),
] + discover_extensions_urlpatterns(MapsConfig.name)
