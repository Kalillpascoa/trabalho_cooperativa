from django.contrib import admin

from .models import (
    Perfil,
    Produto,
    Produtor,
    Estoque,
    Cliente,
    Pedido,
)


class ProdutorAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "fazenda",
        "municipio",
        "saldo",
    )


class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "estoque_total",
        "preco",
    )


class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "email",
        "telefone",
    )


class EstoqueAdmin(admin.ModelAdmin):
    list_display = (
        "produtor",
        "produto",
        "quantidade",
    )


class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "produto",
        "quantidade",
        "valor_total",
        "data",
    )


class PerfilAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "tipo",
    )

    search_fields = (
        "user__username",
    )


admin.site.register(Produtor, ProdutorAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Estoque, EstoqueAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Perfil, PerfilAdmin)