from django.db import migrations, models
import finance.models  # para referenciar gen_ref_code

class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_populate_ref_codes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='ref_code',
            field=models.CharField(
                max_length=50,
                unique=True,
                default=finance.models.gen_ref_code,
                editable=False,
            ),
        ),
    ]
