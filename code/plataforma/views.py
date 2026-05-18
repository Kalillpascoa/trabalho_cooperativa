from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.db.models import DecimalField, Value
import json

from .models import *
from .forms import *


# =========================================
# PÁGINA INICIAL
# =========================================
def pagina_inicial(request):

    return render(
        request,
        'pagina_inicial.html'
    )


# =========================================
# CADASTRO
# =========================================
def register(request):

    if request.method == 'POST':

        form = UsuarioCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            tipo = form.cleaned_data['tipo']

            Perfil.objects.create(
                user=user,
                tipo=tipo
            )

            if tipo == 'PRODUTOR':

                Produtor.objects.create(
                    user=user,
                    nome=user.username,
                    fazenda='Não informado',
                    municipio='Não informado'
                )

            else:

                Cliente.objects.create(
                    user=user,
                    nome=user.username,
                    email='email@email.com',
                    telefone='0000'
                )

            login(request, user)

            return redirect('estoque')

    else:

        form = UsuarioCreationForm()

    return render(
        request,
        'cadastro.html',
        {
            'form': form
        }
    )


# =========================================
# PRODUTORES
# =========================================
@login_required
def produtores(request):

    produtores = Produtor.objects.all()

    return render(
        request,
        'produtores.html',
        {
            'produtores': produtores
        }
    )


# =========================================
# CLIENTES
# =========================================
@login_required
def clientes(request):

    clientes = Cliente.objects.all()

    return render(
        request,
        'clientes.html',
        {
            'clientes': clientes
        }
    )

# =========================================
# PRODUTOS
# =========================================
@login_required
def produtos(request):

    produtos = Produto.objects.all()

    return render(request, 'produtos.html', {
        'produtos': produtos
    })

# =========================================
# PEDIDOS
# =========================================
@login_required
def pedidos(request):

    pedidos = Pedido.objects.select_related(
        'cliente',
        'produto'
    ).all()

    return render(
        request,
        'pedidos.html',
        {
            'pedidos': pedidos
        }
    )


# =========================================
# ESTOQUE
# =========================================
@login_required
def estoque(request):

    # =====================================================
    # GRÁFICO 1
    # ESTOQUE TOTAL POR PRODUTO
    # =====================================================

    estoque_total = (
        Estoque.objects
        .values('produto__nome')
        .annotate(total=Coalesce(Sum('quantidade'), Value(0), output_field=DecimalField()))
    )

    labels = [
        item['produto__nome']
        for item in estoque_total
    ]

    dados = [
        float(item['total'])
        for item in estoque_total
    ]

    # =====================================================
    # GRÁFICO 2
    # ESTOQUE POR PRODUTOR
    # =====================================================

    produtores = Produtor.objects.all()

    estoque_produtores = {}

    for produtor in produtores:

        dados_produtor = (
            Estoque.objects
            .filter(produtor=produtor)
            .values('produto__nome')
            .annotate(total=Coalesce(Sum('quantidade'), Value(0), output_field=DecimalField()))
        )

        estoque_produtores[produtor.nome] = {

            'labels': [
                item['produto__nome']
                for item in dados_produtor
            ],

            'dados': [
                float(item['total'])
                for item in dados_produtor
            ]

        }

    # =====================================================
    # GRÁFICO 3
    # FINANCEIRO
    # =====================================================

    financeiro = {

        'labels': [],
        'potencial': [],
        'disponivel': []

    }

    for produtor in produtores:

        estoques = Estoque.objects.filter(
            produtor=produtor
        )

        potencial = 0

        for item in estoques:

            potencial += (
                float(item.quantidade) *
                float(item.produto.preco)
            )

        # saldo disponível = pedidos vendidos
        vendido = 0

        pedidos_produtor = Pedido.objects.filter(
            produto__estoque__produtor=produtor
        ).distinct()

        for pedido in pedidos_produtor:

            vendido += (
                float(pedido.quantidade) *
                float(pedido.produto.preco)
            )

        financeiro['labels'].append(
            produtor.nome
        )

        financeiro['potencial'].append(
            round(potencial, 2)
        )

        financeiro['disponivel'].append(
            round(vendido, 2)
        )

    # =====================================================
    # ANÁLISE CLIENTES
    # =====================================================

    clientes = Cliente.objects.all()

    analise_clientes = []

    pedidos = Pedido.objects.select_related(
        'cliente',
        'produto'
    )

    for pedido in pedidos:

        total = (
            float(pedido.quantidade) *
            float(pedido.produto.preco)
        )

        analise_clientes.append({

            'cliente': pedido.cliente.nome,

            'produto': pedido.produto.nome,

            'pedidos': int(pedido.quantidade),

            'total': round(total, 2),

            'custo': round(
                float(pedido.produto.preco),
                2
            )

        })

    # =====================================================
    # CONTEXTO
    # =====================================================

    context = {

        'labels': json.dumps(labels),

        'dados': json.dumps(dados),

        'estoque_produtores': json.dumps(
            estoque_produtores
        ),

        'financeiro': json.dumps(
            financeiro
        ),

        'analise_clientes': json.dumps(
            analise_clientes
        ),

        'produtores': produtores,

        'clientes': clientes

    }

    return render(
        request,
        'estoque.html',
        context
    )

# =========================================
# CADASTRAR PRODUTO
# =========================================
@login_required
def cadastrar_produto(request):

    if request.method == 'POST':

        form = ProdutoForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Produto cadastrado com sucesso!'
            )

            return redirect('produtos')

    else:

        form = ProdutoForm()

    return render(
        request,
        'cadastrar_produto.html',
        {'form': form}
    )

# =========================================
# CADASTRAR ESTOQUE
# =========================================
@login_required
def cadastrar_estoque(request):

    if request.method == 'POST':

        form = EstoqueForm(request.POST)

        if form.is_valid():

            estoque = form.save()

            produto = estoque.produto

            produto.estoque_total += estoque.quantidade

            produto.save()

            messages.success(
                request,
                'Produção cadastrada com sucesso!'
            )

            return redirect('estoque')

    else:

        form = EstoqueForm()

    return render(
        request,
        'cadastrar_estoque.html',
        {'form': form}
    )

# =========================================
# CADASTRAR PEDIDO
# =========================================
def cadastrar_pedido(request):

    # Verifica se o usuário está logado
    if not request.user.is_authenticated:

        messages.warning(
            request,
            'Você precisa estar logado para cadastrar um novo pedido.'
        )

        return redirect('login')

    # Verifica se o usuário possui cliente
    try:

        cliente = Cliente.objects.get(
            user=request.user
        )

    except Cliente.DoesNotExist:

        messages.error(
            request,
            'Seu usuário não possui perfil de cliente.'
        )

        return redirect('pagina_inicial')

    if request.method == 'POST':

        form = PedidoForm(request.POST)

        if form.is_valid():

            pedido = form.save(commit=False)

            pedido.cliente = cliente

            produto = pedido.produto

            # Verifica estoque
            if pedido.quantidade > produto.estoque_total:

                messages.error(
                    request,
                    'Estoque insuficiente.'
                )

                return redirect('pedido')

            # Atualiza estoque
            produto.estoque_total -= pedido.quantidade
            produto.save()

            pedido.save()

            messages.success(
                request,
                'Pedido cadastrado com sucesso!'
            )

            return redirect('pedidos')

    else:

        form = PedidoForm()

    return render(
        request,
        'cadastrar_pedidos.html',
        {
            'form': form
        }
    )

