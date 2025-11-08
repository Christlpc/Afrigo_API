from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum, F
from django.core.validators import MinValueValidator

User = get_user_model()


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    pending_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_withdrawal_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wallet'
    
    def __str__(self):
        return f"Wallet de {self.user.email}"
    
    def credit(self, amount, description=None, reference_type=None, reference_id=None):
        """Créditer le wallet"""
        self.balance += amount
        self.total_earned += amount
        self.save()
        
        WalletTransaction.objects.create(
            wallet=self,
            transaction_type='credit',
            amount=amount,
            description=description or f'Recharge de {amount} XAF',
            reference_type=reference_type,
            reference_id=reference_id,
        )
        return self
    
    def debit(self, amount, description=None, reference_type=None, reference_id=None):
        """Débiter le wallet"""
        if self.balance < amount:
            raise ValueError('Solde insuffisant')
        
        self.balance -= amount
        self.save()
        
        WalletTransaction.objects.create(
            wallet=self,
            transaction_type='debit',
            amount=amount,
            description=description or f'Paiement de {amount} XAF',
            reference_type=reference_type,
            reference_id=reference_id,
        )
        return self


class WalletTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Crédit'),
        ('debit', 'Débit'),
        ('commission', 'Commission'),
        ('withdrawal', 'Retrait'),
        ('refund', 'Remboursement'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    reference_type = models.CharField(max_length=50, blank=True, null=True)
    reference_id = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, default='completed')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wallet_transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_type} de {self.amount} XAF - {self.wallet.user.email}"

