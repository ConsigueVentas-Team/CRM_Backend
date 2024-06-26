from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from datetime import timedelta
from api.models import *
from api.serializers.UserSerializer import *     
from datetime import datetime
import os
from django.conf import settings
import glob
#------ AUTHENTICATIONS Views ------#

# Vista para el registro de usuarios
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    
    def upload_image(self):
        try:
            image = self.request.data.get('image')
            if image:
                folder_path = os.path.join(settings.MEDIA_ROOT, 'photos')
                os.makedirs(folder_path, exist_ok=True)
                filename = self.request.data.get('document_number') + '.' + image.name.split('.')[-1]  # Nombre de archivo personalizado
                with open(os.path.join(folder_path, filename), 'wb') as f:
                    f.write(image.read())
                return f'photos/{filename}'
            else:
                # Si no se proporciona ninguna imagen, se devuelve la ruta de la imagen predeterminada
                return f'photos/default.jpeg'
        except Exception as e:
            return Response({"details": f"Error al guardar la imagen: {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def perform_create(self, serializer):
        serializer.validated_data['image'] = self.upload_image()
        # role = Role.objects.get(code_name="employee")
        serializer.save(role=2) #Cuando un usuario se registra por defecto tendra el rol de empleado    
        
# Vista para el login de usuarios
class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            
            access_token = refresh.access_token
            access_token.set_exp(lifetime=timedelta(days=1))
            
            # Obtener los datos del usuario
            user_data = {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'lastname': user.lastname,
            }

            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
                'user': user_data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

#Vista para el Refresh Token
class UserRefreshTokenView(TokenRefreshView):
    def post(self, request):
        refresh_token = request.headers.get('Authorization', '').split(' ')[-1]

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({'error': 'Token de actualización no válido'}, status=401)

        return Response({
            'access': str(serializer.validated_data['access']),
        }) 
        
# Vista para el cambio de contraseña del usuario
class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener el usuario autenticado
        user = self.request.user

        # Verificar la antigua contraseña
        if not user.check_password(serializer.validated_data.get('old_password')):
            return Response({'error': 'La antigua contraseña no es válida.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que la nueva contraseña no sea igual a la antigua
        if serializer.validated_data.get('old_password') == serializer.validated_data.get('new_password'):
            return Response({'error': 'La nueva contraseña debe ser diferente de la antigua'}, status=status.HTTP_400_BAD_REQUEST)

        # Cambiar la contraseña
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()

        return Response({'message': 'Contraseña cambiada exitosamente.'}, status=status.HTTP_200_OK)
    
# Vista para obtener los datos del usuario authenticado
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        # Retorna el usuario authenticado
        return User.objects.filter(pk=self.request.user.pk)
    
    def get_object(self):
        # Retorna el objeto del usuario authenticado
        return self.get_queryset().first()

#------ USER Views ------#

# Vista para el Crear usuarios
class UserCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        # Si es un superusuario, establecer el campo role en None
        role = self.request.data['role']
        print(self.request.data['username'])
        print(self.request.data['password'])
        if(role == 1):
            serializer.save(is_staff=True,is_superuser=True)
        else:
            serializer.save()

class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
    
class UserForIdView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        # No permitir la actualización de la contraseña directamente
        role = request.data.get('role')

        if role is not None:
            serializer = self.get_serializer(instance=self.get_object(), data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            if (role == 1):
                serializer.save(role=1,is_staff=True,is_superuser=True) #Asignar como administrador
            elif (role == 2):
                serializer.save(role=2,is_staff=False,is_superuser=False) #Quitar el rol de administrador

            return Response(serializer.data)
         
        else:
            pass
        if 'password' in request.data:
            return Response({'error': 'No se puede actualizar la contraseña directamente.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar la foto del usuario
        if 'image' in request.data:
            image = request.data.get('image')
            folder_path = os.path.join(settings.MEDIA_ROOT, 'photos')
            os.makedirs(folder_path, exist_ok=True)
            user_instance = self.get_object()
            # Eliminar imagen anterior
            if user_instance.image:
                previous_image_path = os.path.join(settings.MEDIA_ROOT, 'photos', user_instance.document_number + '.*')
                previous_images = glob.glob(previous_image_path)
                for prev_image in previous_images:
                    if os.path.exists(prev_image):
                        os.remove(prev_image)
            filename = user_instance.document_number + '.' + image.name.split('.')[-1]
            with open(os.path.join(folder_path, filename), 'wb') as f:
                f.write(image.read())
            user_instance.image = f'photos/{filename}'
            user_instance.save()
        return super().update(request, *args, **kwargs)
    
class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False  # Desactivar la cuenta
        instance.save()
        return Response({'detail': 'La cuenta ha sido desactivada.'}, status=status.HTTP_200_OK)