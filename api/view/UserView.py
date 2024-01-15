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

#------ AUTHENTICATIONS Views ------#

# Vista para el registro de usuarios
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        role = Role.objects.get(code_name="employee")
        serializer.save(role=role) #Cuando un usuario se registra por defecto tendra el rol de empleado
        
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
                'email': user.email,
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
        role = Role.objects.get(id=self.request.data['role'])

        if(role.code_name == "admin"):
            serializer.save(is_staff=True,is_superuser=True)
        else:
            serializer.save()

class UserListPagination(PageNumberPagination):
    page_size = 10  # Número de elementos por página
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserListPagination
    def get_queryset(self):
        # Filtra solo los usuarios con is_active=True
        return User.objects.filter(is_active=True)
        
    
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
        try:
            role = Role.objects.get(pk=int(request.data['role'])) 
            serializer = self.get_serializer(instance=self.get_object(), data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            if (role.code_name == 'admin'):
                serializer.save(role=role,is_staff=True,is_superuser=True) #Asignar como administrador
            elif (role.code_name == 'employee'):
                serializer.save(role=role,is_staff=False,is_superuser=False) #Quitar el rol de administrador

            return Response(serializer.data)
        except Role.DoesNotExist:
            pass


        if 'password' in request.data:
            return Response({'error': 'No se puede actualizar la contraseña directamente.'}, status=status.HTTP_400_BAD_REQUEST)
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