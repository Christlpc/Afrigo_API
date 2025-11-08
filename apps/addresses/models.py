from django.contrib.gis.db import models as gis_models
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    address_label = models.CharField(max_length=100, blank=True, null=True)
    full_address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    location = gis_models.PointField(srid=4326, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'addresses'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.full_address
    
    def save(self, *args, **kwargs):
        # Créer le point PostGIS si latitude et longitude sont fournis
        if self.latitude and self.longitude and not self.location:
            from django.contrib.gis.geos import Point
            self.location = Point(float(self.longitude), float(self.latitude), srid=4326)
        super().save(*args, **kwargs)

