from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_superuser',
            # Resident fields:
            'user_country', 'user_state', 'user_district', 'user_city', 'user_ward',
            # Include any other fields as needed
        ]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data  # ✅ Ensure user_data includes is_superuser
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data  # ✅ Now includes is_superuser
            }
        raise serializers.ValidationError("Invalid credentials")