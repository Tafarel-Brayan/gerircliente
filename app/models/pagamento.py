from django.db import models
from .cobranca import Cobranca
from django.core.validators import MinValueValidator
from decimal import Decimal


class Pagamento(models.Model):
    """Class representing a payment made by a client for a billing."""

    FORMA_PAGAMENTO_CHOICES = (
        ('PIX', 'Pix'),
        ('CARTAO', 'Cartão'),
        ('DINHEIRO', 'Dinheiro'),
        ('TRANSFERENCIA', 'Transferência'),
    )

    cobranca = models.OneToOneField(
        Cobranca,
        on_delete=models.PROTECT,
        related_name='pagamento'
    )

    data_pagamento = models.DateTimeField(auto_now_add=True)

    valor_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES
    )

    comprovante = models.FileField(
        upload_to='comprovantes/%Y/%m/',
        null=True,
        blank=True
    )

    observacao = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'pagamento'
        ordering = ['-data_pagamento']

    def __str__(self):
        return f"Pagamento {self.id} - {self.cobranca.cliente.nome} - R$ {self.valor_pago}"

    def save(self, *args, **kwargs):
        # Atualiza o status da cobrança quando um pagamento é registrado
        self.cobranca.status = 'PAGO'
        self.cobranca.save()
        super().save(*args, **kwargs)
