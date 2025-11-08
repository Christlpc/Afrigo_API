from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone

from .models import Wallet, WalletTransaction
from .serializers import WalletSerializer, WalletTransactionSerializer, RechargeSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_balance(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    serializer = WalletSerializer(wallet)
    return Response({
        'success': True,
        'message': 'Solde récupéré avec succès',
        'data': {
            'balance': float(wallet.balance),
            'wallet': serializer.data
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def recharge(request):
    serializer = RechargeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    amount = serializer.validated_data['amount']
    
    # Créditer le wallet
    wallet.credit(
        amount=amount,
        description=f'Recharge de portefeuille de {amount} XAF',
        reference_type='recharge'
    )
    
    return Response({
        'success': True,
        'message': 'Portefeuille rechargé avec succès',
        'data': {
            'transaction': WalletTransactionSerializer(wallet.transactions.first()).data,
            'newBalance': float(wallet.balance)
        }
    }, status=status.HTTP_200_OK)


class TransactionListView(generics.ListAPIView):
    serializer_class = WalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        return WalletTransaction.objects.filter(wallet=wallet)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Transactions récupérées avec succès',
            'data': {
                'transactions': serializer.data
            }
        })

