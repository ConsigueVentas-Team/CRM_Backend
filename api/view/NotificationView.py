from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api. model.NotificationModel import Notification
from api.serializers.NotificationSerializer import NotificationSerializer

#Listar y crear 
class NotificationListCreate(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    """ permission_classes = [IsAuthenticated] """

#Detalle, actualizar y eliminar 
class NotificationDetailUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    """ permission_classes = [IsAuthenticated] """