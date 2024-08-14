from django.db import models
import uuid

class Payment(models.Model):
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('COMPLETO', 'Completo'),
        ('FALHOU', 'Falhou'),
    )

    order_id = models.IntegerField("ID do Pedido")
    amount = models.DecimalField("Valor", max_digits=10, decimal_places=2)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    transaction_id = models.UUIDField("ID da Transação", default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"Pagamento {self.transaction_id} - Pedido {self.order_id}"

    def mark_as_completed(self):
        """Marcar o pagamento como completo."""
        self.status = 'COMPLETO'
        self.save()

    def mark_as_failed(self):
        """Marcar o pagamento como falhou."""
        self.status = 'FALHOU'
        self.save()
