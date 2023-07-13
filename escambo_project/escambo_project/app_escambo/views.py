
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import *
from django.contrib import messages
from .models import *
from .dao import *

import random


def index(request): 
    dao = genericaDao()
    return render(request, 'escambo/index.html', dao.listarProdutosCategorias())

def cadastroUsuario(request):
    if request.method == 'POST':
        dao = usuarioDao()
        if dao.cadastrarUsuario(request.POST, request.FILES):
            messages.success(request, 'aí sim! cadastro realizado com sucesso! faça login para ter acesso a plataforma')      
            return redirect('escambo:login')
    return render(request, 'escambo/cadastro.html', {'form': CadastroForm()})


def cadastrar_produto(request):
    if request.method == 'POST':
        dao = produtoDao()
       
        if dao.cadastrarProduto(request.POST, request.FILES):            
            return redirect('escambo:index')  # Redirecionar para a página detalhes do produto após o cadastro
    
    return render(request, 'escambo/publicar_produto.html', {'form': ProdutoForm()})

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
                return index(request)
            else:
                messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
    else:        
        mensagem = messages.get_messages(request)
        form = LoginForm()   
        context = {
            'mensagem': mensagem,
            'form': form
        }
    return render(request, 'escambo/login.html', context)

def logout_view(request):
    logout(request)
    return index(request)