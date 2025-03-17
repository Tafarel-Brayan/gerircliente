# app/admin/cobranca_admin.py
from django.contrib import admin
from django.utils.html import format_html
from ..models.cobranca import Cobranca


@admin.register(Cobranca)
class CobrancaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'data_vencimento',
        'valor_formatado',
        'status_colorido',
        'descricao',
        'data_criacao'
    )

    list_filter = (
        'status',
        'data_vencimento',
        'data_criacao'
    )

    search_fields = (
        'cliente__nome',
        'cliente__email',
        'descricao'
    )

    readonly_fields = ('data_criacao',)

    ordering = ('-data_vencimento',)

    list_per_page = 20

    actions = ['marcar_como_pago', 'marcar_como_cancelado']

    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'cliente',
                'valor',
                'data_vencimento',
                'descricao'
            )
        }),
        ('Status', {
            'fields': (
                'status',
            )
        }),
        ('Informações do Sistema', {
            'fields': (
                'data_criacao',
            ),
            'classes': ('collapse',)
        }),
    )

    def valor_formatado(self, obj):
        return f'R$ {obj.valor:.2f}'.replace('.', ',')
    valor_formatado.short_description = 'Valor'

    def status_colorido(self, obj):
        cores = {
            'PENDENTE': 'orange',
            'PAGO': 'green',
            'ATRASADO': 'red',
            'CANCELADO': 'gray'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            cores[obj.status],
            obj.get_status_display()
        )
    status_colorido.short_description = 'Status'

    @admin.action(description='Marcar selecionados como PAGO')
    def marcar_como_pago(self, request, queryset):
        atualizados = queryset.update(status='PAGO')
        self.message_user(
            request,
            f'{atualizados} cobrança(s) marcada(s) como PAGO.'
        )

    @admin.action(description='Marcar selecionados como CANCELADO')
    def marcar_como_cancelado(self, request, queryset):
        atualizados = queryset.update(status='CANCELADO')
        self.message_user(
            request,
            f'{atualizados} cobrança(s) marcada(s) como CANCELADO.'
        )

    def get_queryset(self, request):
        """Otimiza as queries usando select_related"""
        return super().get_queryset(request).select_related('cliente')

    def save_model(self, request, obj, form, change):
        """Atualiza o status ao salvar se necessário"""
        super().save_model(request, obj, form, change)
        obj.atualizar_status()
