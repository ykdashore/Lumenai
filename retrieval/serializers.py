from rest_framework import serializers
from .models import PdfDocument

class PdfDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdfDocument
        fields = ['id', 'user', 'title', 'file', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
