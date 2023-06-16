from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import UsuarioForm, CadastroForm, LoginForm 
from django.contrib import messages
from .models import Produto,Categoria, Usuario

import random

# Create your views here.
def index(request):
    produtos = Produto.objects.all().order_by('-id')
    categorias = Categoria.objects.all() 
    usuarios = Usuario.objects.all()  

    template = loader.get_template('escambo/index.html')
    context = { 
        'produtos': produtos,
        'categorias': categorias,
        'usuarios': usuarios,
    }  
    return HttpResponse(template.render(context, request))

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            cpf = form.cleaned_data['cpf']
            endereco = form.cleaned_data['endereco']
            telefone = form.cleaned_data['telefone']
            foto = form.cleaned_data['foto']

             # Verificar se o nome de usuário já existe
            if User.objects.filter(username=username).exists():
                # Lidar com o caso de nome de usuário duplicado
                # (exibir uma mensagem de erro, redirecionar, etc.)

                return HttpResponse('Nome de usuário já está em uso')
            user = User.objects.create_user(username=username, password=password)
            new_user = Usuario.objects.create(user=user, cpf=cpf, endereco=endereco, telefone=telefone, foto=foto)
            new_user.save()
            return redirect('escambo:index')
        else:
            form = CadastroForm()
    else:
        form = CadastroForm()
    
    return render(request, 'escambo/cadastro.html', {'form': form})

from app_escambo.forms import ProdutoForm

def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('escambo:index')  # Redirecionar para a página inicial após o cadastro
    else:
        form = ProdutoForm()
 


    return render(request, 'escambo/publicar_produto.html', {'form': form})

def pesquisar_produtos(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            produtos = Produto.objects.filter(nome__icontains=query)
        else:
            produtos = Produto.objects.all()
        
        context = {
            'produtos': produtos,
            'query': query
        }
        return render(request, 'escambo/pesquisar_produtos.html', context)
    
def pesquisar_por_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    produtos = Produto.objects.filter(categoria=categoria)

    context = {
        'categoria': categoria,
        'produtos': produtos
    }

    return render(request, 'escambo/pesquisar_por_categoria.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('perfil_usuario')  # Redirecionar para a página do perfil do usuário após o login
            else:
                messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')