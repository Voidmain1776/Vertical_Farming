from django.urls import path

from . import views
from .views import (latestSensorData, liveRecordsSensorData, CropPredictionAPI)

urlpatterns = [
    path("", views.index, name="index"),
    path("latestSensorData",latestSensorData.as_view(), name="latestSensorData"),
    path("liveRecordsSensorData",liveRecordsSensorData.as_view(), name="liveRecordsSensorData"),
    path("CropPredictionAPI",CropPredictionAPI.as_view(), name="CropPredictionAPI")
]


