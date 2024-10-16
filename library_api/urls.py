from django.contrib import admin

from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

schema_view = get_schema_view(
   title="Library API",
   description="API documentation for the Naveen's HCL Library System. Hey Saurabh and Uzma, I was trying with Swagger, getting some errors, as I don't have much time, have documented in DRF format. Thanks.",
   version="1.0.0",
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/', include('books.urls')),  # Include your app's URLs here
   path('schema/', schema_view, name='api-schema'),  # Schema endpoint
]

