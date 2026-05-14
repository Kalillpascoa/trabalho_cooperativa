from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    # Página inicial
    path('', views.pagina_inicial, name='pagina_inicial'),

    # Cadastro
    path('cadastro/', views.register, name='cadastro'),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # Produtores
    path(
        'produtores/',
        views.produtores,
        name='produtores'
    ),

    # Clientes
    path(
        'clientes/',
        views.clientes,
        name='clientes'
    ),

    # Produtos
    path(
        'produtos/',
        views.produtos,
        name='produtos'
    ),

    # Pedidos
    path(
        'pedidos/',
        views.pedidos,
        name='pedidos'
    ),

    # Cadastro de pedido
    path(
        'pedido/',
        views.cadastrar_pedido,
        name='pedido'
    ),

    # Estoque
    path(
        'estoque/',
        views.estoque,
        name='estoque'
    ),
]