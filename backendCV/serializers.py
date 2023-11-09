from rest_framework import serializers
from backendCV.models import Employee, Company, User

# Serializer CompanyListSerializer para el modelo Company
class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__' # Incluye todos los campos del modelo Company


# Serializer EmployeeListSerializer para el modelo Employee
class EmployeeListSerializer(serializers.ModelSerializer):
    
    company_name = serializers.CharField(source='company_id.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['user_id','nombre','apellidos','email','company_id','company_name']
        

# Serializer para el modelo User (para registro)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellidos', 'email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# Serializer para el modelo User (para login)
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
