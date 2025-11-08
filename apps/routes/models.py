from django.contrib.gis.db import models as gis_models
from django.contrib.auth import get_user_model
from django.db import models
from decimal import Decimal

User = get_user_model()


class Route(models.Model):
    ROUTE_TYPE_CHOICES = [
        ('taxi', 'Taxi'),
        ('moto', 'Moto'),
        ('vip', 'VIP'),
        ('carpool', 'Covoiturage'),
    ]
    
    VIP_CLASS_CHOICES = [
        ('business', 'Business'),
        ('luxe', 'Luxe'),
        ('xl', 'XL'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('pickup', 'Prise en charge'),
        ('in_transit', 'En transit'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Espèces'),
        ('mobile_money', 'Mobile Money'),
        ('card', 'Carte'),
        ('wallet', 'Portefeuille'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('cancelled', 'Annulé'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name='routes_as_client')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='routes_as_driver', null=True, blank=True)
    pickup_address = models.ForeignKey('addresses.Address', on_delete=models.PROTECT, related_name='pickup_routes')
    dropoff_address = models.ForeignKey('addresses.Address', on_delete=models.PROTECT, related_name='dropoff_routes')
    pickup_location = gis_models.PointField(srid=4326, null=True, blank=True)
    dropoff_location = gis_models.PointField(srid=4326, null=True, blank=True)
    route_type = models.CharField(max_length=20, choices=ROUTE_TYPE_CHOICES)
    vip_class = models.CharField(max_length=20, choices=VIP_CLASS_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    cancelled_by = models.CharField(max_length=50, blank=True, null=True)
    
    # Distance et durée
    estimated_distance = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    estimated_duration = models.IntegerField(null=True, blank=True)  # en minutes
    actual_distance = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    actual_duration = models.IntegerField(null=True, blank=True)
    
    # Tarification
    base_fare = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    distance_fare = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    time_fare = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    traffic_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    weather_surcharge = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    waiting_fee = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    vip_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    total_fare = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    driver_earnings = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Paiement
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Informations supplémentaires
    notes = models.TextField(blank=True, null=True)
    third_party_order = models.BooleanField(default=False)
    third_party_name = models.CharField(max_length=100, blank=True, null=True)
    third_party_phone = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'routes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Route {self.id} - {self.client.email}"
    
    def save(self, *args, **kwargs):
        # Créer les points PostGIS si latitude/longitude sont fournis
        if self.pickup_address and not self.pickup_location:
            if self.pickup_address.latitude and self.pickup_address.longitude:
                from django.contrib.gis.geos import Point
                self.pickup_location = Point(
                    float(self.pickup_address.longitude),
                    float(self.pickup_address.latitude),
                    srid=4326
                )
        
        if self.dropoff_address and not self.dropoff_location:
            if self.dropoff_address.latitude and self.dropoff_address.longitude:
                from django.contrib.gis.geos import Point
                self.dropoff_location = Point(
                    float(self.dropoff_address.longitude),
                    float(self.dropoff_address.latitude),
                    srid=4326
                )
        
        super().save(*args, **kwargs)

