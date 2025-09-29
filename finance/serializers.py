from rest_framework import serializers
from .models import Expense, Payment

class ExpenseSerializer(serializers.ModelSerializer):
    resident_id = serializers.IntegerField(source='resident.id', read_only=True)

    class Meta:
        model = Expense
        fields = ('id','resident_id','period','amount','status','due_date','created_at')

class PaymentSerializer(serializers.ModelSerializer):
    expense_detail = ExpenseSerializer(source='expense', read_only=True)

    class Meta:
        model = Payment
        fields = ('id','expense','amount','method','ref_code','paid_at','expense_detail')

class StatementSerializer(serializers.Serializer):
    pending_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    paid_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    items = ExpenseSerializer(many=True)
