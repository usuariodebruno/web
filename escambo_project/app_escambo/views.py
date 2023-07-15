
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import *
from django.contrib import messages
from .models import *
from .dao import *



#FAZER
def index(request): 
    dao = genericaDao()
    return render(request, 'escambo/index.html', dao.listarProdutosCategorias())

#FAZER
def cadastroUsuario(request):
    if request.method == 'POST':
        dao = usuarioDao()

        if dao.cadastrarUsuario(request.POST, request.FILES):
            messages.success(request, 'aí sim! cadastro realizado com sucesso! faça login para ter acesso a plataforma')      
            return redirect('escambo:login')
        
    return render(request, 'escambo/cadastro.html', {'form': CadastroForm()})

#FAZER
def cadastrar_produto(request):
    if request.method == 'POST':
        dao = produtoDao()
       
        if dao.cadastrarProduto(request.POST, request.FILES):            
            return redirect('escambo:index')  # Redirecionar para a página detalhes do produto após o cadastro
    
    return render(request, 'escambo/publicar_produto.html', {'form': ProdutoForm()})

#Fazer
def pesquisar_produtos(request):
    dao = produtoDao()

    if request.method == 'GET':       
        return render(request, 'escambo/pesquisar_produtos.html',  dao.pequisarProduto(request))

#FAZER
def pesquisar_por_categoria(request, categoria_id):
    dao = produtoDao()

    return render(request, 'escambo/pesquisar_por_categoria.html', dao.buscarPorCategoria(categoria_id))

#FAZER
def logout_view(request):
    logout(request)
    return index(request)

#FAZER
def detalhe_produto(request,**kwargs):
    dao = produtoDao()

    return render(request, 'escambo/detalhe_produto.html', dao.detalharProduto(kwargs.get('produto_id')))

#TRETA
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
            mensagem = messages.get_messages(request)
            form = LoginForm()   
            context = {
                'mensagem': messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.'),
                'form': form
            }
            return render(request, 'escambo/login.html', context)
        
    form = LoginForm()
    return render(request, 'escambo/login.html', { 'form': form})

"""
def login_view(request):  
    dao = loginDao()  
    if request.method == 'POST':
        retorno = dao.login(request)
        if retorno is not None:
            login(request, user=retorno)
            return index(request)
        else: 
            return render(request, 'escambo/login.html', retorno)
        
    form = LoginForm()
    return render(request, 'escambo/login.html', { 'form': form})
"""