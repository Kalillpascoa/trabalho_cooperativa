from django.contrib import admin

from .models import (
    Perfil,
    Produto,
    Produtor,
    Estoque,
    Cliente,
    Pedido,
)

# =========================================
# INLINE ESTOQUE
# =========================================

class EstoqueInline(admin.TabularInline):

    model = Estoque
    extra = 1


# =========================================
# PRODUTOR
# =========================================

@admin.register(Produtor)
class ProdutorAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "fazenda",
        "municipio",
        "saldo",
    )

    search_fields = (
        "nome",
        "fazenda",
        "municipio",
    )

    list_filter = (
        "municipio",
    )

    inlines = [EstoqueInline]


# =========================================
# PRODUTO
# =========================================

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "estoque_total",
        "preco",
    )

    search_fields = (
        "nome",
    )

    list_filter = (
        "preco",
    )


# =========================================
# CLIENTE
# =========================================

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "email",
        "telefone",
    )

    search_fields = (
        "nome",
        "email",
    )


# =========================================
# ESTOQUE
# =========================================

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):

    list_display = (
        "produtor",
        "produto",
        "quantidade",
    )

    search_fields = (
        "produtor__nome",
        "produto__nome",
    )

    list_filter = (
        "produto",
        "produtor",
    )


# =========================================
# PEDIDOS
# =========================================

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        "cliente",
        "produto",
        "quantidade",
        "valor_total",
        "data",
    )

    search_fields = (
        "cliente__nome",
        "produto__nome",
    )

    list_filter = (
        "data",
        "produto",
    )


# =========================================
# PERFIL
# =========================================

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "tipo",
    )

    search_fields = (
        "user__username",
    )

    list_filter = (
        "tipo",
    )