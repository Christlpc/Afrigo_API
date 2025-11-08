from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Générer le token JWT
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'Inscription réussie',
            'data': {
                'user': UserSerializer(user).data,
                'token': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.user
        if user.status != 'active':
            return Response({
                'success': False,
                'message': 'Votre compte n\'est pas actif'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        tokens = serializer.validated_data
        
        return Response({
            'success': True,
            'message': 'Connexion réussie',
            'data': {
                'user': UserSerializer(user).data,
                'token': tokens['access'],
                'refresh': tokens['refresh'],
            }
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_profile(request):
    serializer = UserSerializer(request.user)
    return Response({
        'success': True,
        'message': 'Profil récupéré avec succès',
        'data': serializer.data
    })

