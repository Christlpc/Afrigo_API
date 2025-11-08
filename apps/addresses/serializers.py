from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_digits=10, decimal_places=8, required=True)
    longitude = serializers.DecimalField(max_digits=11, decimal_places=8, required=True)
    
    class Meta:
        model = Address
        fields = ['id', 'address_label', 'full_address', 'latitude', 'longitude',
                  'city', 'district', 'postcode', 'additional_info', 'is_favorite',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("La latitude doit être entre -90 et 90")
        return value
    
    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("La longitude doit être entre -180 et 180")
        return value


class AddressUpdateFavoriteSerializer(serializers.Serializer):
    is_favorite = serializers.BooleanField()

