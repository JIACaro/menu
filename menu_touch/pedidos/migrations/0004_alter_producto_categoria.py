# Generated by Django 5.0.4 on 2024-10-30 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.CharField(choices=[('Platos', 'Platos'), ('Bebestibles', 'Bebestibles'), ('Acompañamiento', 'Acompañamiento'), ('Postres', 'Postres')], max_length=50),
        ),
    ]