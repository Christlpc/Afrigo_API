from rest_framework import serializers
from .models import Route
from apps.addresses.serializers import AddressSerializer


class RouteSerializer(serializers.ModelSerializer):
    pickup_address = AddressSerializer(read_only=True)
    dropoff_address = AddressSerializer(read_only=True)
    
    class Meta:
        model = Route
        fields = ['id', 'client', 'driver', 'pickup_address', 'dropoff_address',
                  'route_type', 'vip_class', 'status', 'scheduled_at',
                  'third_party_order', 'third_party_name', 'third_party_phone',
                  'estimated_distance', 'estimated_duration',
                  'base_fare', 'distance_fare', 'time_fare', 'total_fare',
                  'commission_amount', 'driver_earnings',
                  'payment_method', 'payment_status', 'notes',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'client', 'driver', 'status', 'created_at', 'updated_at']


class RouteCreateSerializer(serializers.Serializer):
    pickupAddressId = serializers.IntegerField()
    dropoffAddressId = serializers.IntegerField()
    pickupLatitude = serializers.DecimalField(max_digits=10, decimal_places=8)
    pickupLongitude = serializers.DecimalField(max_digits=11, decimal_places=8)
    dropoffLatitude = serializers.DecimalField(max_digits=10, decimal_places=8)
    dropoffLongitude = serializers.DecimalField(max_digits=11, decimal_places=8)
    routeType = serializers.ChoiceField(choices=['taxi', 'moto', 'vip', 'carpool'])
    vipClass = serializers.ChoiceField(choices=['business', 'luxe', 'xl'], required=False, allow_null=True)
    scheduledAt = serializers.DateTimeField(required=False, allow_null=True)
    thirdPartyOrder = serializers.BooleanField(required=False, default=False)
    thirdPartyName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    thirdPartyPhone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    def validate(self, attrs):
        if attrs.get('routeType') == 'vip' and not attrs.get('vipClass'):
            raise serializers.ValidationError({"vipClass": "vipClass est requis pour les routes VIP"})
        return attrs
    
    def to_internal_value(self, data):
        # Convertir camelCase en snake_case pour la validation interne
        internal_data = {}
        mapping = {
            'pickupAddressId': 'pickup_address_id',
            'dropoffAddressId': 'dropoff_address_id',
            'pickupLatitude': 'pickup_latitude',
            'pickupLongitude': 'pickup_longitude',
            'dropoffLatitude': 'dropoff_latitude',
            'dropoffLongitude': 'dropoff_longitude',
            'routeType': 'route_type',
            'vipClass': 'vip_class',
            'scheduledAt': 'scheduled_at',
            'thirdPartyOrder': 'third_party_order',
            'thirdPartyName': 'third_party_name',
            'thirdPartyPhone': 'third_party_phone',
        }
        
        for key, value in data.items():
            internal_key = mapping.get(key, key)
            internal_data[internal_key] = value
        
        return super().to_internal_value(internal_data)
