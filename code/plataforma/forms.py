from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class UsuarioCreationForm(UserCreationForm):
    tipo = forms.ChoiceField(
        choices=[
            ('PRODUTOR', 'Produtor'),
            ('CLIENTE', 'Cliente')
        ]
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'tipo']


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'quantidade']


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['produto', 'quantidade']