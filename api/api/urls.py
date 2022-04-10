from django.urls import path

from .views import UploadFileView, EncodeFileView, DecodeFileView

urlpatterns = [
    path('upload', UploadFileView.as_view()),
    path('encode', EncodeFileView.as_view()),
    path('decode', DecodeFileView.as_view())
]