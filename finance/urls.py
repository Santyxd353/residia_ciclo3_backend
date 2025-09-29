# backend/finance/urls.py
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from .views import (
    StatementView, MyPaymentsView, PayView,
    ReportsView, GenerateMonthlyView, NotifyDueView,
    MyExpensesList
)

urlpatterns = [
    re_path(r'^finance/statement/?$', StatementView.as_view(), name='finance-statement'),
    re_path(r'^finance/pay/?$', PayView.as_view(), name='finance-pay'),
    re_path(r'^finance/reports/?$', ReportsView.as_view(), name='finance-reports'),
    re_path(r'^finance/generate/?$', GenerateMonthlyView.as_view(), name='finance-generate'),
    re_path(r'^finance/notify-due/?$', NotifyDueView.as_view(), name='finance-notify-due'),
    re_path(r'^finance/expenses/?$', MyExpensesList.as_view(), name='finance-expenses'),
]

router = DefaultRouter()
router.register(r'finance/payments', MyPaymentsView, basename='payments')
urlpatterns += router.urls
