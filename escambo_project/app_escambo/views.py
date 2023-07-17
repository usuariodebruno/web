
from audioop import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import *
from django.contrib import messages
from .models import *
from .dao import *
import sys



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
@login_required(redirect_field_name='next', login_url="/login/")
def cadastrar_produto(request):
    if request.method == 'POST':
        dao = produtoDao()
       
        if dao.cadastrarProduto(request, request.FILES):            
            return redirect('escambo:index')    
    
    form = ProdutoForm()
    return render(request, 'escambo/publicar_produto.html', {'form': form})

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
'''
#FAZER
def detalhe_produto(request, produto_id):
    dao = produtoDao()
    return render(request, 'escambo/detalhe_produto.html', dao.detalharProduto(produto_id))

@login_required(redirect_field_name='next', login_url="/login/")
def selecionar_produtos_cesta(request, *args, **kwargs):
    #Produto interesse
    produto = get_object_or_404(Produto, id=kwargs['produto_id']) 
   
    # Escambador do produto selecionado
    outro_escambador_cesta = produto.usuario_proprietario 

    # Escambador do logado
    escambador_logado = request.user.escambador 
    produtos_usuario_logado = Produto.objects.filter(usuario_proprietario=escambador_logado)
    
    if request.method == 'POST':
        # Cesta do outro usuario
        outro_escambador_cesta = Cesta.objects.create(escambador_dono=outro_escambador_cesta)
        outro_escambador_cesta.produto.add(produto)
        outro_escambador_cesta.save()
        #print('cesta do outro usuario', outro_escambador_cesta)

        # Cesta usuario logado
        usuario_logado_cesta = Cesta.objects.create(escambador_dono=escambador_logado)
        produtos_usuario_logado = request.POST.getlist('produtos')

        for produto_logado in produtos_usuario_logado:
            usuario_logado_cesta.produto.add(produto_logado)

        usuario_logado_cesta.save()
        
        #print('cesta do usuario logado', usuario_logado_cesta)
        #print("------------ enviou")
        escambo = Escambo()
        context = {
            'outro_escambador_cesta': outro_escambador_cesta,
            'usuario_logado_cesta': usuario_logado_cesta,
        }
        
        return render(request, 'escambo/meus_escambos.html', context )
'''
#FAZER
def detalhe_produto(request, produto_id):
    dao = produtoDao()
    return render(request, 'escambo/detalhe_produto.html', dao.detalharProduto(produto_id))

@login_required(redirect_field_name='next', login_url="/login/")
def selecionar_produtos_cesta(request, *args, **kwargs):
    #Produto interesse
    produto = get_object_or_404(Produto, id=kwargs['produto_id']) 
    # Escambador do produto selecionado
    outro_escambador = produto.usuario_proprietario 

    # Escambador do logado
    escambador_logado = request.user.escambador 
    produtos_usuario_logado = Produto.objects.filter(usuario_proprietario=escambador_logado)
    
    if request.method == 'POST':
        
        # Cesta do outro usuario
        outro_escambador_cesta = Cesta.objects.create(escambador_dono=outro_escambador)
        outro_escambador_cesta.produto.add(produto)
        outro_escambador_cesta.save()

        # Cesta usuario logado
        usuario_logado_cesta = Cesta.objects.create(escambador_dono=escambador_logado)
        produtos_usuario_logado = request.POST.getlist('produtos')

        for produto_logado in produtos_usuario_logado:
            usuario_logado_cesta.produto.add(produto_logado)
        usuario_logado_cesta.save()    

        escambo = Escambo.objects.create(escambo_ativo=True, usuario_iniciou= request.user.escambador.id)
        escambo.cestas.add(usuario_logado_cesta, outro_escambador_cesta)
        dao = cestaDao()
        escambo.qnt_itens = (usuario_logado_cesta.produto.count()) + (outro_escambador_cesta.produto.count())

        escambo.usuarios.add(outro_escambador_cesta.escambador_dono, usuario_logado_cesta.escambador_dono)
        escambo.confirmado_usuario_iniciou = True
        escambo.save()

        return redirect('escambo:meus_escambos')

@login_required(redirect_field_name='next', login_url="/login/")
def meus_escambos(request): 
    dao = escamboDao()  

    escambador_logado = request.user.escambador
    escambos_usuario = Escambo.objects.filter(usuarios=escambador_logado)
    print(escambos_usuario)
    
    #escambo iniciados por outra pessoa
    escambos_solicitados = Escambo.objects.exclude(usuario_iniciou=escambador_logado.id).filter(usuarios=escambador_logado)
    print(escambos_solicitados)

    escambos_usuario = escambos_usuario.exclude(id__in=escambos_solicitados.values_list('id', flat=True))
    print(escambos_usuario) 

    #escambos_inativos
    escambos_inativos = Escambo.objects.filter(usuarios=escambador_logado, escambo_ativo=False)

    # Remover escambos inativos de escambos_usuario
    escambos_usuario = escambos_usuario.exclude(id__in=escambos_inativos)

    # Remover escambos inativos de escambos_solicitados
    escambos_solicitados = escambos_solicitados.exclude(id__in=escambos_inativos)


    context = {
        'meus_escambos': escambos_usuario,
        'escambos_solicitados': escambos_solicitados,  
        'escambos_inativos': escambos_inativos,      
    }

    return render(request, 'escambo/meus_escambos.html', context ) 

@login_required(redirect_field_name='next', login_url="/login/")
def selecionar_produtos_teste(request, **kwargs):
    produto = get_object_or_404(Produto, id=kwargs['produto_id']) #Produto interesse   

    # Escambador do logado
    escambador_logado = request.user.escambador 
    produtos_usuario_logado = Produto.objects.filter(usuario_proprietario=escambador_logado)
 
    if request.method == 'POST':      
            context = {
                'produto': produto,
                'produtos_usuario_logado': produtos_usuario_logado,
                'usuario_logado': escambador_logado
            }
            return render(request, 'escambo/escambo_selecao.html', context)       
        
@login_required(redirect_field_name='next', login_url="/login/")
def excluir_produto(request, **kwargs):
    produto = get_object_or_404(Produto, id=kwargs['produto_id']) #Produto para exluir
    print(kwargs['produto_id'])
    if request.method == 'POST':
        produto.delete()
        return redirect('escambo:index')
    
def finalizar_escambo(request, **kwargs):
    escambo = get_object_or_404(Escambo, id=kwargs['escambo_id'])  

    escambo.confirmado_usuario_outro = True
    escambo.escambo_ativo = False
    dao = escamboDao()
    if dao.todos_confirmados(escambo):
        escambo.save()
        # Passar pelos produtos das cestas do escambo e mudar status_trocado dos produtos para True
        for cesta in escambo.cestas.all():
            for produto in cesta.produto.all():
                produto.status_trocado = True
                produto.save()
        return render(request, 'escambo/escambo_sucesso.html')    
    return HttpResponse("Erro ao finalizadar escambo!")

def meus_produtos(request):  
    dao = produtoDao()
    p = dao.buscarProdutosUsuario(request.user.escambador)
    context = {
        'produtos': p
    }

    return render(request, 'escambo/meus_produtos.html', context)
def teste(request):       
        return render(request, 'escambo/escambo_sucesso.html') 
#FAZER
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
