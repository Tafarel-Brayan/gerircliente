from django.contrib import admin
from ..models.pagamento import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cobranca',
        'data_pagamento',
        'valor_pago',
        'forma_pagamento',
        'comprovante',
        'observacao',
    )

    list_filter = (
        'forma_pagamento',
    )

    search_fields = (
        'cobranca__cliente__nome',
        'cobranca__descricao',
    )

    readonly_fields = ('data_pagamento',)
    ordering = ('-data_pagamento',)

    list_per_page = 20
