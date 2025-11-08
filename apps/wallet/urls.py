from django.urls import path
from .views import get_balance, recharge, TransactionListView

urlpatterns = [
    path('balance/', get_balance, name='balance'),
    path('recharge/', recharge, name='recharge'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
]

