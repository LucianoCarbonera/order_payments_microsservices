# Generated by Django 5.1 on 2024-08-14 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(verbose_name='ID do Pedido')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),
                ('status', models.CharField(default='PENDENTE', max_length=20, verbose_name='Status')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='ID da Transação')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
        ),
    ]