from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 
                  'user_type', 'status', 'kyc_status', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, min_length=9)
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    userType = serializers.ChoiceField(choices=['client', 'driver', 'merchant', 'livreur'], required=False)
    firstName = serializers.CharField(required=False, allow_blank=True)
    lastName = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Les mots de passe ne correspondent pas"})
        
        # Vérifier si l'email existe
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Cet email est déjà utilisé"})
        
        # Vérifier si le téléphone existe
        if User.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError({"phone": "Ce numéro de téléphone est déjà utilisé"})
        
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        user_type = validated_data.pop('userType', 'client')
        first_name = validated_data.pop('firstName', None)
        last_name = validated_data.pop('lastName', None)
        
        user = User.objects.create_user(
            password=password,
            user_type=user_type,
            first_name=first_name,
            last_name=last_name,
            **validated_data
        )
        
        # Créer le profil client si nécessaire
        if user.user_type == 'client':
            from apps.accounts.models import ClientProfile
            from apps.wallet.models import Wallet
            ClientProfile.objects.create(user=user)
            Wallet.objects.create(user=user)
        
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = user.user_type
        token['email'] = user.email
        return token

