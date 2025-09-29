from django.db import migrations
import uuid

def gen_ref():
    return f"PAY-{uuid.uuid4().hex[:10].upper()}"

def forwards(apps, schema_editor):
    Payment = apps.get_model('finance', 'Payment')
    seen = set()
    for p in Payment.objects.all().only('id', 'ref_code'):
        if not p.ref_code:
            code = gen_ref()
            while code in seen or Payment.objects.filter(ref_code=code).exists():
                code = gen_ref()
            p.ref_code = code
            p.save(update_fields=['ref_code'])
            seen.add(code)

def backwards(apps, schema_editor):
    Payment = apps.get_model('finance', 'Payment')
    Payment.objects.update(ref_code=None)

class Migration(migrations.Migration):

    dependencies = [
        # 👇 Usa exactamente el nombre del archivo 0002 que ves en tu carpeta, sin ".py"
        ('finance', '0002_alter_expense_options_alter_payment_options_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
