
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import *

from django.views import View

from .forms import *
from .models import *
from .dao import *

class EscabadorView(View):
    # Atualizado
    def cadastroUsuario(request):
        if request.method == 'POST':
            dao = usuarioDao()

            if dao.cadastrarUsuario(request.POST, request.FILES):
                messages.success(request, 'aí sim! cadastro realizado com sucesso! faça login para ter acesso a plataforma')      
                return redirect('escambo:login')
            
        return render(request, 'escambo/cadastro.html', {'form': CadastroForm()})
    
     # Atualizado
    def index(request): 
        dao = produtoDao()
        return render(request, 'escambo/index.html', dao.listarProdutosCategorias())
    
    

   
class ProdutoView(View):
    # Atualizado
    @login_required(redirect_field_name='next', login_url="/login/")
    def cadastrar_produto(request):
        if request.method == 'POST':
            dao = produtoDao()
        
            if dao.cadastrarProduto(request, request.FILES):            
                return redirect('escambo:index')    
        
        form = ProdutoForm()
        return render(request, 'escambo/publicar_produto.html', {'form': form})

    # Atualizado
    def pesquisar_produtos(request):
        dao = produtoDao()

        if request.method == 'GET':       
            return render(request, 'escambo/pesquisar_produtos.html',  dao.pequisarProduto(request))

    # Atualizado
    def pesquisar_por_categoria(request, categoria_id):
        dao = produtoDao()

        return render(request, 'escambo/pesquisar_por_categoria.html', dao.buscarPorCategoria(categoria_id))

    # Atualizado
    def detalhe_produto(request, produto_id):
        dao = produtoDao()
        return render(request, 'escambo/detalhe_produto.html', dao.detalharProduto(produto_id))
    # Atualizado
    def meus_produtos(request):  
        dao = produtoDao()
        p = dao.buscarProdutosUsuario(request.user.escambador)
        context = {
            'produtos': p
        }

        return render(request, 'escambo/meus_produtos.html', context)
    
    # Pendente
    @login_required(redirect_field_name='next', login_url="/login/")
    def excluir_produto(request, **kwargs):
        produto = get_object_or_404(Produto, id=kwargs['produto_id']) #Produto para exluir
        print(kwargs['produto_id'])
        dao = produtoDao()
        dao.de
        if request.method == 'POST':
            produto.delete()
            return redirect('escambo:index')

class EscaboView(View):
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
    
    # Atualizado
    @login_required(redirect_field_name='next', login_url="/login/")
    def abrir_escambo(request, *args, **kwargs):
        daoCesta = cestaDao()

        # Produto interesse
        produto = get_object_or_404(Produto, id=kwargs['produto_id']) 
        

        # Escambador do produto selecionado
        outro_escambador = produto.usuario_proprietario 

        if request.method == 'POST':
            
            # Cesta do outro usuario escambador, produtos
            c1 = daoCesta.criar_cesta(outro_escambador, produto)   

            # Cesta usuario logado          
            c2 = daoCesta.criar_cesta(request.user.escambador, request.POST.getlist('produtos'))

            daoEscambo = escamboDao()
            daoEscambo.criar_escambo(request.user.escambador, c1, c2)

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

class CestaView(View):
    # Atualizado
    @login_required(redirect_field_name='next', login_url="/login/")
    def selecionar_produtos(request, **kwargs):
        produto = get_object_or_404(Produto, id=kwargs['produto_id']) #Produto interesse   

        dao = produtoDao()
    
        if request.method == 'POST':      
            context = {
                'produto': produto,
                'produtos_usuario_logado': dao.buscarProdutosEscambador(request.user.escambador),
                'usuario_logado': request.user.escambador
            }
            return render(request, 'escambo/escambo_selecao.html', context)       
        
    
# Pendente
def login_view(request):  
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                return EscabadorView.index(request)
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

    # Atualizado
def logout_view(request):
    logout(request)
    return redirect('escambo:index')