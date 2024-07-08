from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .schema import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apps.common.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
