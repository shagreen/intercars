from django.urls import path, include

from bank.views.account import (
    AccountCreateView,
    AccountDashboardView,
    AccountDepositView,
    AccountTransferHistoryView,
    AccountTransferView,
    AccountUpdateView
)

users_patterns = [
    path('create/', AccountCreateView.as_view(), name='create'),
    path('dashboard/', AccountDashboardView.as_view(), name='dashboard'),
    path('deposit/', AccountDepositView.as_view(), name='deposit'),
    path('transfer_history/', AccountTransferHistoryView.as_view(), name='account transfer history'),
    path('<str:account_iban>/update/', AccountUpdateView.as_view(), name='update'),
    path('make_transfer/', AccountTransferView.as_view(), name='make transfer'),
]

urlpatterns = [
    path('', include((users_patterns, 'account'))),
]
