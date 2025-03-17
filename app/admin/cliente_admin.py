from django.contrib import admin
from ..models.cliente import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email', 'telefone')
    search_fields = ('nome', 'cpf', 'email', 'telefone')
    list_filter = ('cidade', 'estado')
    ordering = ('nome',)
