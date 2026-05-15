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
