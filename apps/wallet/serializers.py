from rest_framework import serializers
from .models import Wallet, WalletTransaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'pending_balance', 'total_earned', 
                  'last_withdrawal_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = ['id', 'transaction_type', 'amount', 'description', 
                  'reference_type', 'reference_id', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class RechargeSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=100)
    
    def validate_amount(self, value):
        if value < 100:
            raise serializers.ValidationError("Le montant minimum de recharge est de 100 XAF")
        return value

