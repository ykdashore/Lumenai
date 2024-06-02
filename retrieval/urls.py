from django.urls import path, include
from retrieval import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'upload', views.UploadDocument, basename='upload-document')

urlpatterns = router.urls