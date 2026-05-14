from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

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

    return render(
        request,
        'produtos.html',
        {
            'produtos': produtos
        }
    )


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
# CADASTRAR PEDIDO
# =========================================
@login_required
def cadastrar_pedido(request):

    cliente = Cliente.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        form = PedidoForm(request.POST)

        if form.is_valid():

            pedido = form.save(commit=False)

            pedido.cliente = cliente

            produto = pedido.produto

            if pedido.quantidade > produto.estoque_total:

                messages.error(
                    request,
                    'Estoque insuficiente'
                )

                return redirect('pedido')

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
        'cadastro_pedido.html',
        {
            'form': form
        }
    )


# =========================================
# ESTOQUE
# =========================================
@login_required
def estoque(request):

    produtos = Produto.objects.all()

    produtores = Produtor.objects.all()

    labels = []
    dados = []

    for produto in produtos:

        labels.append(produto.nome)

        dados.append(float(produto.estoque_total))

    estoque_produtores = {}

    for produtor in produtores:

        estoque_produtores[produtor.nome] = {
            'labels': [],
            'dados': []
        }

        estoques = Estoque.objects.filter(
            produtor=produtor
        )

        for estoque in estoques:

            estoque_produtores[produtor.nome]['labels'].append(
                estoque.produto.nome
            )

            estoque_produtores[produtor.nome]['dados'].append(
                float(estoque.quantidade)
            )

    context = {
        'labels': labels,
        'dados': dados,
        'estoque_produtores': estoque_produtores,
        'produtores': produtores
    }

    return render(
        request,
        'estoque.html',
        context
    )