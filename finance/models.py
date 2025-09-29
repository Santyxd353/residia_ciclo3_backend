import uuid
from django.db import models
from django.conf import settings
from residents.models import Resident

def gen_ref_code():
    return f"PAY-{uuid.uuid4().hex[:10].upper()}"

class Expense(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        PAID = 'PAID', 'Pagado'

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='expenses')
    period = models.CharField(max_length=7)  # "YYYY-MM"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('resident', 'period')
        ordering = ['-period', '-created_at']

class Payment(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='payments')
    paid_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, default='ONLINE')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # ==== TEMPORAL: SIN unique y permisivo ====
    ref_code = models.CharField(
        max_length=50,
        unique=False,       # <- temporal
        null=True, blank=True,
        default=None,
        editable=False
    )
    # ==========================================

    class Meta:
        ordering = ['-paid_at']
