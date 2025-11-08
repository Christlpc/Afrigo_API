from decimal import Decimal
from django.conf import settings


class PricingService:
    """Service de calcul des tarifs"""
    
    @staticmethod
    def calculate_fare(route_type, distance_km, duration_minutes, vip_class=None,
                      traffic_multiplier=1.0, weather_surcharge=0, waiting_fee=0):
        """
        Calcule le tarif d'un trajet
        """
        config = settings.PRICING_CONFIG.get(route_type)
        if not config:
            raise ValueError(f"Type de route invalide: {route_type}")
        
        multiplier = Decimal('1.0')
        
        # Appliquer le multiplicateur VIP si applicable
        if route_type == 'vip' and vip_class:
            vip_multipliers = settings.VIP_MULTIPLIERS
            multiplier *= Decimal(str(vip_multipliers.get(vip_class, 1.0)))
        
        # Calcul des composantes du tarif
        base_fare = Decimal(str(config['base_fare'])) * multiplier
        distance_fare = Decimal(str(distance_km)) * Decimal(str(config['per_km_rate'])) * multiplier * Decimal(str(traffic_multiplier))
        time_fare = Decimal(str(duration_minutes)) * Decimal(str(config['per_minute_rate'])) * multiplier
        
        # Calcul du tarif total
        total_fare = base_fare + distance_fare + time_fare + Decimal(str(weather_surcharge)) + Decimal(str(waiting_fee))
        
        # Appliquer le tarif minimum
        minimum_fare = Decimal(str(config['minimum_fare'])) * multiplier
        if total_fare < minimum_fare:
            total_fare = minimum_fare
        
        return {
            'base_fare': float(base_fare),
            'distance_fare': float(distance_fare),
            'time_fare': float(time_fare),
            'vip_multiplier': float(multiplier) if route_type == 'vip' and vip_class else 1.0,
            'total_fare': float(total_fare),
        }
    
    @staticmethod
    def estimate_distance_and_duration(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng):
        """
        Estime la distance et la durée d'un trajet (formule Haversine)
        """
        from math import radians, sin, cos, atan2, sqrt
        
        R = 6371  # Rayon de la Terre en km
        
        d_lat = radians(dropoff_lat - pickup_lat)
        d_lon = radians(dropoff_lng - pickup_lng)
        lat1 = radians(pickup_lat)
        lat2 = radians(dropoff_lat)
        
        a = sin(d_lat / 2) ** 2 + sin(d_lon / 2) ** 2 * cos(lat1) * cos(lat2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = R * c
        
        # Estimation de la durée (vitesse moyenne de 30 km/h en ville)
        average_speed_kmh = 30
        duration_minutes = (distance_km / average_speed_kmh) * 60
        
        return {
            'distance_km': round(distance_km, 2),
            'duration_minutes': round(duration_minutes),
        }
    
    @staticmethod
    def calculate_commission(total_fare, commission_rate=None):
        """
        Calcule la commission de la plateforme
        """
        if commission_rate is None:
            commission_rate = settings.COMMISSION_RATE
        return float(Decimal(str(total_fare)) * Decimal(str(commission_rate)) / Decimal('100'))

