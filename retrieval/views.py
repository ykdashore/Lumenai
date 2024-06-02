from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from .models import *
from .serializers import PdfDocumentSerializer
from rest_framework.parsers import MultiPartParser, FormParser



class UploadDocument(viewsets.ModelViewSet):
    queryset = PdfDocument.objects.all()
    serializer_class = PdfDocumentSerializer
    parserer_class = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
