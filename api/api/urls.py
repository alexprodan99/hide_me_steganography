from django.urls import path

from .views import FileView

urlpatterns = [
    path('upload', FileView.as_view()),
    path('download/<id>', FileView.as_view())
]