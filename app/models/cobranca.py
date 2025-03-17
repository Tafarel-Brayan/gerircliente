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

    @classmethod
    def criar_cobrancas_mensais(cls, cliente, valor, quantidade_meses, dia_vencimento, descricao_base):
        if dia_vencimento < 1 or dia_vencimento > 31:
            raise ValueError("Dia de vencimento deve estar entre 1 e 31")

        if quantidade_meses < 1:
            raise ValueError("Quantidade de meses deve ser maior que zero")

        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")

        # Verifica se já existem cobranças para o período
        data_inicial = timezone.now().date()
        data_inicial = data_inicial.replace(day=dia_vencimento)
        data_final = data_inicial + relativedelta(months=quantidade_meses)

        cobrancas_existentes = cls.objects.filter(
            cliente=cliente,
            data_vencimento__range=[data_inicial, data_final]
        ).exists()

        if cobrancas_existentes:
            raise ValueError(
                "Já existem cobranças cadastradas para este período")

        # Continua com a criação das cobranças...
