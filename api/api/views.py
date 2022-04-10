import os
import cv2
import mimetypes
from .algorithms import *
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import FileSerializer
from .models import File


class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file = file_serializer.save()
            
            response_data = {
                'id' : file.id,
                'timestamp' : file_serializer.data['timestamp']
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DecodeFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, *args, **kwargs):
        if 'id' not in request.GET:
            return Response({'message' : 'There are missing args'}, status=status.HTTP_404_NOT_FOUND)
        file = File.objects.filter(id=request.GET['id'])
        
        if file.exists():
            file_name = file[0].file
            file_path = f"{settings.MEDIA_ROOT}/{file_name}"
            
            if not os.path.exists(file_path):
                return Response({'message' : 'Specified file does not exists'}, status=status.HTTP_404_NOT_FOUND)
            image = cv2.imread(file_path)
            
            decoded_text = show_data(image)
            return Response(data={'text' : decoded_text}, status=status.HTTP_200_OK)
        else:
            return Response({'message' : 'Specified file does not exists'}, status=status.HTTP_404_NOT_FOUND)
    

class EncodeFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, *args, **kwargs):
        
        if 'id' not in request.GET or 'secret_text' not in request.GET:
            return Response({'message' : 'There are missing args'}, status=status.HTTP_404_NOT_FOUND)

        file = File.objects.filter(id=request.GET['id'])
        
        secret_text = request.GET['secret_text']
        
        if file.exists():
            file_name = file[0].file
            file_path = f"{settings.MEDIA_ROOT}/{file_name}"
            
            if not os.path.exists(file_path):
                return Response({'message' : 'Specified file does not exists'}, status=status.HTTP_404_NOT_FOUND)
            response = Response({}, status=status.HTTP_200_OK)
            
            image = cv2.imread(file_path)
            
            encoded_image = hide_data(image, secret_text)
            cv2.imwrite(file_path, encoded_image)
            with open(file_path, "rb") as file:
                mime_type = mimetypes.guess_type(file_path)
                response = HttpResponse(file, content_type=mime_type)
                response['Content-Disposition'] = "attachment; filename=%s" % (file_name)
            
            return response
        else:
            return Response({'message' : 'Specified file does not exists'}, status=status.HTTP_404_NOT_FOUND)
        