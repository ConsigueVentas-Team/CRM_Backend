from rest_framework import generics
from django.contrib.auth.models import Permission
from api.serializers.PermissionsSerializer import PermissionSerializer
# Listar permisos
class PermissionsListView(generics.ListAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()