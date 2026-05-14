from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Perfil(models.Model):
    TIPOS = (
        ('PRODUTOR', 'Produtor'),
        ('CLIENTE', 'Cliente'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.nome


class Produtor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    fazenda = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    saldo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.nome


class Estoque(models.Model):
    produtor = models.ForeignKey(Produtor, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        total = Estoque.objects.filter(
            produto=self.produto
        ).aggregate(
            models.Sum('quantidade')
        )['quantidade__sum'] or Decimal('0')

        self.produto.estoque_total = total
        self.produto.save()

    def __str__(self):
        return f"{self.produtor.nome} - {self.produto.nome}"


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    quantidade = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    valor_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    data = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        self.valor_total = self.quantidade * self.produto.preco

        super().save(*args, **kwargs)

        estoques = Estoque.objects.filter(
            produto=self.produto
        )

        total_produto = estoques.aggregate(
            models.Sum('quantidade')
        )['quantidade__sum'] or Decimal('0')

        if total_produto <= 0:
            return

        for estoque in estoques:

            percentual = estoque.quantidade / total_produto

            valor_produtor = Decimal(percentual) * self.valor_total

            estoque.produtor.saldo += valor_produtor
            estoque.produtor.save()

            estoque.quantidade -= Decimal(percentual) * self.quantidade

            if estoque.quantidade < 0:
                estoque.quantidade = 0

            estoque.save()

        novo_estoque = Estoque.objects.filter(
            produto=self.produto
        ).aggregate(
            models.Sum('quantidade')
        )['quantidade__sum'] or Decimal('0')

        self.produto.estoque_total = novo_estoque
        self.produto.save()

    def __str__(self):
        return f"Pedido #{self.id}"