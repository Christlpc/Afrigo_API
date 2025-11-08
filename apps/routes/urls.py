from django.urls import path
from .views import RouteListCreateView, RouteDetailView, cancel_route, pay_with_wallet

urlpatterns = [
    path('', RouteListCreateView.as_view(), name='route-list-create'),
    path('<int:pk>/', RouteDetailView.as_view(), name='route-detail'),
    path('<int:pk>/cancel/', cancel_route, name='route-cancel'),
    path('<int:pk>/pay-wallet/', pay_with_wallet, name='route-pay-wallet'),
]

