from django.urls import path
from .views import AddressListCreateView, update_favorite

urlpatterns = [
    path('', AddressListCreateView.as_view(), name='address-list-create'),
    path('<int:pk>/favorite/', update_favorite, name='address-update-favorite'),
]

