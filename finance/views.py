import uuid
from datetime import date
from decimal import Decimal
from django.db.models import Sum
from django.utils.timezone import now
from rest_framework import permissions, status, views, response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import generics


from .models import Expense, Payment
from .serializers import ExpenseSerializer, PaymentSerializer, StatementSerializer
from residents.models import Resident

def get_my_resident(user):
    # Admin ve todo; residente sólo su registro
    if user.is_superuser or getattr(user, 'role', '') == 'ADMIN':
        return None
    return Resident.objects.filter(user=user).first()

class StatementView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        me_res = get_my_resident(request.user)
        if me_res:
            qs = Expense.objects.filter(resident=me_res)
        else:
            # admin puede filtrar por ?resident_id=#
            rid = request.query_params.get('resident_id')
            qs = Expense.objects.filter(resident_id=rid) if rid else Expense.objects.none()

        items = qs.order_by('-period','-created_at')
        pending_total = qs.filter(status='PENDING').aggregate(s=Sum('amount'))['s'] or Decimal('0.00')
        paid_total = qs.filter(status='PAID').aggregate(s=Sum('amount'))['s'] or Decimal('0.00')

        ser = StatementSerializer({
            'pending_total': pending_total,
            'paid_total': paid_total,
            'items': items
        }, context={'request': request})
        return response.Response(ser.data)

class MyPaymentsView(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        me_res = get_my_resident(self.request.user)
        if me_res:
            return Payment.objects.filter(expense__resident=me_res)
        # admin puede ver por residente con ?resident_id=#
        rid = self.request.query_params.get('resident_id')
        return Payment.objects.filter(expense__resident_id=rid) if rid else Payment.objects.none()

class PayView(views.APIView):
    """
    CU8 – Pago online simulado:
    body: { "expense_id": 1, "method": "ONLINE" }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        expense_id = request.data.get('expense_id')
        method = request.data.get('method', 'ONLINE')

        exp = Expense.objects.filter(id=expense_id).select_related('resident__user').first()
        if not exp:
            return response.Response({'detail':'Expense no encontrada'}, status=404)

        # sólo dueño (residente) de esa expensa o admin
        me_res = get_my_resident(request.user)
        if me_res and exp.resident_id != me_res.id:
            return response.Response({'detail':'Forbidden'}, status=403)

        if exp.status == 'PAID':
            return response.Response({'detail':'Esta expensa ya está pagada'}, status=400)

        # simular aprobación de pasarela
        ref = f'PAY-{uuid.uuid4().hex[:10].upper()}'
        p = Payment.objects.create(
            expense=exp,
            method=method,
            amount=exp.amount,
            ref_code=ref
        )
        exp.status = 'PAID'
        exp.save(update_fields=['status'])

        return response.Response(PaymentSerializer(p).data, status=201)

class ReportsView(views.APIView):
    """
    CU10 – Reporte simple (admin): ?period=YYYY-MM
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not (request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN'):
            return response.Response({'detail':'Forbidden'}, status=403)

        period = request.query_params.get('period')
        qs = Expense.objects.all()
        if period:
            qs = qs.filter(period=period)

        total_pend = qs.filter(status='PENDING').aggregate(s=Sum('amount'))['s'] or Decimal('0.00')
        total_paid = qs.filter(status='PAID').aggregate(s=Sum('amount'))['s'] or Decimal('0.00')
        count_exp = qs.count()

        return response.Response({
            'period': period,
            'count_expenses': count_exp,
            'total_pending': str(total_pend),
            'total_paid': str(total_paid),
        })

class GenerateMonthlyView(views.APIView):
    """
    Utilidad para generar expensas del mes (admin):
    body: {"period":"2025-09","amount":"300.00","due_date":"2025-09-30"}
    Crea Expense PENDING para todos los residentes que tengan unidad.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not (request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN'):
            return response.Response({'detail':'Forbidden'}, status=403)

        period = request.data.get('period')
        amount = Decimal(request.data.get('amount','0.00'))
        due = request.data.get('due_date')

        res_qs = Resident.objects.exclude(unit__isnull=True)
        created = 0
        for r in res_qs:
            obj, was_created = Expense.objects.get_or_create(
                resident=r, period=period,
                defaults={'amount': amount, 'due_date': due}
            )
            if was_created:
                created += 1

        return response.Response({'period': period, 'created': created}, status=201)

class NotifyDueView(views.APIView):
    """
    CU11 – Notificaciones de vencimiento (simples a consola).
    En producción: integrar email/sms/push. Aquí solo simula.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not (request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN'):
            return response.Response({'detail':'Forbidden'}, status=403)

        today = now().date()
        soon = Expense.objects.filter(status='PENDING', due_date__isnull=False, due_date__gte=today)
        count = 0
        for e in soon.select_related('resident__user'):
            user = e.resident.user
            # Simulación (imprimir consola / log)
            print(f"[NOTIFY] {user.email} – Expensa {e.period} vence el {e.due_date}")
            count += 1

        return response.Response({'sent': count})
class MyExpensesList(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    def get_queryset(self):
        me_res = get_my_resident(self.request.user)
        if me_res:
            return Expense.objects.filter(resident=me_res).order_by('-period', '-created_at')
        rid = self.request.query_params.get('resident_id')
        return Expense.objects.filter(resident_id=rid) if rid else Expense.objects.none()