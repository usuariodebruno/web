from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

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
        model = Escambador
        fields = ('cpf', 'endereco', 'telefone', 'foto')

class CadastroForm(forms.Form):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    cpf = forms.CharField(max_length=14, required=False)
    endereco = forms.CharField(max_length=255)
    telefone = forms.CharField(max_length=20, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']
        cpf = self.cleaned_data['cpf']
        endereco = self.cleaned_data['endereco']
        telefone = self.cleaned_data['telefone']
        foto = self.cleaned_data['foto']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Nome de usuário já está em uso.")

        user = User.objects.create_user(username=username, password=password)

        escambador = Escambador.objects.create(
            user=user,
            cpf=cpf,
            endereco=endereco,
            telefone=telefone,
            foto=foto,
        )

        return escambador

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao_afetiva', 'estado_produto', 'categoria', 'usuario_proprietario']
        widgets = {
            'descricao_afetiva': forms.Textarea(attrs={'rows': 4}),
        }
