from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Route
from .serializers import RouteSerializer, RouteCreateSerializer
from .services import PricingService
from .permissions import IsClient
from apps.addresses.models import Address
from apps.wallet.models import Wallet

User = get_user_model()


class RouteListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsClient]
    
    def get_queryset(self):
        return Route.objects.filter(client=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RouteCreateSerializer
        return RouteSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = RouteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Récupérer les adresses
        pickup_address = get_object_or_404(Address, id=serializer.validated_data['pickup_address_id'])
        dropoff_address = get_object_or_404(Address, id=serializer.validated_data['dropoff_address_id'])
        
        # Créer la route
        route = Route.objects.create(
            client=request.user,
            pickup_address=pickup_address,
            dropoff_address=dropoff_address,
            route_type=serializer.validated_data['route_type'],
            vip_class=serializer.validated_data.get('vip_class'),
            scheduled_at=serializer.validated_data.get('scheduled_at'),
            third_party_order=serializer.validated_data.get('third_party_order', False),
            third_party_name=serializer.validated_data.get('third_party_name'),
            third_party_phone=serializer.validated_data.get('third_party_phone'),
            notes=serializer.validated_data.get('notes'),
        )
        
        # Calculer la distance et la durée
        pricing_data = PricingService.estimate_distance_and_duration(
            float(serializer.validated_data['pickup_latitude']),
            float(serializer.validated_data['pickup_longitude']),
            float(serializer.validated_data['dropoff_latitude']),
            float(serializer.validated_data['dropoff_longitude']),
        )
        
        # Calculer le tarif
        fare = PricingService.calculate_fare(
            route.route_type,
            pricing_data['distance_km'],
            pricing_data['duration_minutes'],
            route.vip_class
        )
        
        # Calculer la commission
        commission_rate = 15  # 15%
        commission_amount = PricingService.calculate_commission(fare['total_fare'], commission_rate)
        driver_earnings = fare['total_fare'] - commission_amount
        
        # Mettre à jour la route avec les informations de tarification
        route.estimated_distance = pricing_data['distance_km']
        route.estimated_duration = pricing_data['duration_minutes']
        route.base_fare = fare['base_fare']
        route.distance_fare = fare['distance_fare']
        route.time_fare = fare['time_fare']
        route.total_fare = fare['total_fare']
        route.commission_amount = commission_amount
        route.commission_rate = commission_rate
        route.driver_earnings = driver_earnings
        route.vip_multiplier = fare['vip_multiplier']
        route.save()
        
        return Response({
            'success': True,
            'message': 'Commande créée avec succès',
            'data': {
                'route': RouteSerializer(route).data
            }
        }, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = RouteSerializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Commandes récupérées avec succès',
            'data': {
                'routes': serializer.data
            }
        })


class RouteDetailView(generics.RetrieveAPIView):
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]
    
    def get_queryset(self):
        return Route.objects.filter(client=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Commande récupérée avec succès',
            'data': {
                'route': serializer.data
            }
        })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsClient])
def cancel_route(request, pk):
    route = get_object_or_404(Route, pk=pk, client=request.user)
    
    if route.status in ['completed', 'cancelled']:
        return Response({
            'success': False,
            'message': 'Cette commande ne peut pas être annulée'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    route.status = 'cancelled'
    route.cancelled_at = timezone.now()
    route.cancelled_by = 'client'
    route.save()
    
    # Rembourser si payé avec le wallet
    if route.payment_method == 'wallet' and route.payment_status == 'completed':
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        wallet.credit(
            amount=route.total_fare,
            description=f'Remboursement pour annulation de commande #{route.id}',
            reference_type='route',
            reference_id=route.id
        )
    
    return Response({
        'success': True,
        'message': 'Commande annulée avec succès',
        'data': {
            'route': RouteSerializer(route).data
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsClient])
def pay_with_wallet(request, pk):
    route = get_object_or_404(Route, pk=pk, client=request.user)
    
    if route.payment_status == 'completed':
        return Response({
            'success': False,
            'message': 'Cette commande est déjà payée'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not route.total_fare:
        return Response({
            'success': False,
            'message': 'Le tarif n\'a pas été calculé'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Débiter le wallet
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    try:
        wallet.debit(
            amount=route.total_fare,
            description=f'Paiement pour commande #{route.id}',
            reference_type='route',
            reference_id=route.id
        )
    except ValueError as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Mettre à jour le statut de paiement
    route.payment_method = 'wallet'
    route.payment_status = 'completed'
    route.save()
    
    return Response({
        'success': True,
        'message': 'Paiement effectué avec succès',
        'data': {
            'route': RouteSerializer(route).data
        }
    })

