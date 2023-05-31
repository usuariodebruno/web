from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario, Produto

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UsuarioForm(UserCreationForm):
    cpf = forms.CharField(max_length=14)
    endereco = forms.CharField(max_length=255)
    telefone = forms.CharField(max_length=20)
    foto = forms.ImageField(required=False)

    class Meta:
        model = Usuario
        fields = ('cpf', 'endereco', 'telefone', 'foto')

class CadastroForm(forms.Form):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    cpf = forms.CharField(max_length=14)
    endereco = forms.CharField(max_length=255)
    telefone = forms.CharField(max_length=20)
    foto = forms.ImageField(required=False)

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
