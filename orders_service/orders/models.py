from django.db import models

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendente'),
        ('COMPLETED', 'Concluído'),
        ('CANCELLED', 'Cancelado'),
    )

    order_id = models.AutoField(primary_key=True)
    product_name = models.CharField("Nome do Produto", max_length=255)
    quantity = models.IntegerField("Quantidade")
    price = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"Pedido {self.order_id} - {self.product_name}"

    @property
    def total_price(self):
        """Retorna o preço total com base na quantidade e preço unitário."""
        return self.quantity * self.price

    def mark_as_completed(self):
        """Método para marcar o pedido como concluído."""
        self.status = 'COMPLETED'
        self.save()

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']
