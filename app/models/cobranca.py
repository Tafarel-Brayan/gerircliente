from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from dateutil.relativedelta import *


class Cobranca(models.Model):
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    )

    TIPO_CHOICES = (
        ('PACOTE', 'Pacote'),
        ('SENHA_EXTRA', 'Senha Extra'),
    )

    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.PROTECT,
        related_name='cobrancas'
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='PACOTE'
    )

    data_vencimento = models.DateField()
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    descricao = models.CharField(max_length=200)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cobranca'
        ordering = ['data_vencimento']

    def __str__(self):
        return f"Cobrança {self.id} - {self.cliente.nome} - R$ {self.valor}"

    def esta_atrasado(self):
        return self.status == 'PENDENTE' and self.data_vencimento < timezone.now().date()

    def atualizar_status(self):
        if self.status == 'PENDENTE' and self.esta_atrasado():
            self.status = 'ATRASADO'
            self.save()
