from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import CadastroForm, LoginForm, ProdutoForm
from django.contrib import messages
from .models import Produto,Categoria, Escambador

import random

def index(request):
    produtos = Produto.objects.all().order_by('-id')
    categorias = Categoria.objects.all() 

    template = loader.get_template('escambo/index.html')
    context = { 
        'produtos': produtos,
        'categorias': categorias,
    }

    return HttpResponse(template.render(context, request))

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST, request.FILES)
        if form.is_valid():
            escambador = form.save()
            return redirect('escambo:index')
    else:
        form = CadastroForm()

    return render(request, 'escambo/cadastro.html', {'form': form})


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
                return index(request)
            else:
                messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
    else:
        form = LoginForm()
    return render(request, 'escambo/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return index(request)