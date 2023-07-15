from django import forms
from django.contrib.auth.forms import UserCreationForm
from multiupload.fields import MultiFileField
from django.contrib.auth.models import User
from .models import *

from django.contrib.auth.forms import AuthenticationForm
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
    foto = forms.ImageField(required=False) 
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        
        return cleaned_data

class ProdutoForm(forms.ModelForm):
    fotos = MultiFileField(min_num=1, max_num=6, max_file_size=1024 * 1024 * 5)

    class Meta:
        model = Produto
        fields = ['nome', 'descricao_afetiva', 'estado_produto', 'categoria', 'destaque', 'usuario_proprietario', 'fotos']

   
