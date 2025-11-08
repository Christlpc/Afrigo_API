from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Address
from .serializers import AddressSerializer, AddressUpdateFavoriteSerializer


class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'message': 'Adresse créée avec succès',
            'data': {
                'address': serializer.data
            }
        }, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Adresses récupérées avec succès',
            'data': {
                'addresses': serializer.data
            }
        })


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_favorite(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    serializer = AddressUpdateFavoriteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    address.is_favorite = serializer.validated_data['is_favorite']
    address.save()
    
    return Response({
        'success': True,
        'message': 'Adresse mise à jour avec succès',
        'data': {
            'address': AddressSerializer(address).data
        }
    })

