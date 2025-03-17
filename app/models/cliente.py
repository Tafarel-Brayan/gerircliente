from django.db import models

class Cliente(models.Model):
  nome = models.CharField(max_length=100)  # Nome do cliente
  email = models.EmailField(unique=True)   # Email obrigatório e exclusivo
  telefone = models.CharField(max_length=15)  # Telefone obrigatório
  rg = models.CharField(max_length=20, blank=True, null=True)  # RG opcional
  cpf = models.CharField(max_length=14, unique=True)  # CPF exclusivo
  endereco = models.CharField(max_length=255, blank=True, null=True)  # Endereço opcional
  cidade = models.CharField(max_length=100, blank=True, null=True)  # Cidade opcional
  estado = models.CharField(max_length=2, blank=True, null=True)  # Estado (Ex.: SP, RJ)
  cep = models.CharField(max_length=10, blank=True, null=True)  # CEP opcional
  bairro = models.CharField(max_length=100, blank=True, null=True)  # Bairro opcional

  def __str__(self):
      return f"{self.nome} - CPF: {self.cpf}"  # Retorna o nome como representação do cliente

  class Meta:
     db_table = 'cliente'