from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from random import shuffle
from django import forms
from .models import *
from .forms import *
    
class produtoDao:
    def cadastrarProduto(self, r, rfile):
        form = ProdutoForm(r.POST, rfile)
        if form.is_valid():
            produto = form.save(commit=False)
            escambador = Escambador.objects.get(user=r.user) 
            produto.usuario_proprietario = escambador
            # produto.usuario_proprietario = escambador  # Define o valor do campo 'usuario_proprietario' com o usuário logado
            #produto.save()
            return self.save(form.cleaned_data, escambador)
    
    def detalharProduto(self, id_produto):
        produto = Produto.objects.get(id=id_produto)
        dao = categoriaDao()
        context = {
            'produto': produto,
            'categorias': dao.buscarCategorias()
        }
        return context
    
    def buscarPorCategoria(self, categoria_id):
        categoria = Categoria.objects.get(id=categoria_id)
        produtos = Produto.objects.filter(categoria=categoria).order_by('-id')

        context = {
            'categoria': categoria,
            'produtos': produtos
        }
        return context
    
    def buscarProdutosEscambador(self, escambador):
        return Produto.objects.filter(usuario_proprietario=escambador)
    
    def pequisarProduto(self, r):
        palavra = r.GET.get('query')
        if palavra:
            produtos = Produto.objects.filter(nome__icontains=palavra)
        else:
            produtos = Produto.objects.all()
        
        context = {
            'produtos': produtos,
            'palavra': palavra
        }

        return context
    
    def save(self, cleaned_data, escambador):
        nome = cleaned_data['nome']
        descricao_afetiva = cleaned_data['descricao_afetiva']
        estado_produto = cleaned_data['estado_produto']
        categoria = cleaned_data['categoria']
        destaque = cleaned_data['destaque']

        produto = Produto.objects.create(
            nome=nome,
            descricao_afetiva=descricao_afetiva,
            estado_produto=estado_produto,
            categoria=categoria,
            usuario_proprietario=escambador,
            destaque=destaque
        )
        
                  
        if produto.destaque == True:
            escambador.ativos = escambador.ativos - 1
            escambador.save()        

        for image in cleaned_data['fotos']:
            Foto.objects.create(produto=produto, imagem=image)

        return produto
    
    def buscarProdutosUsuario(self, escambador):
        produtos = Produto.objects.filter(usuario_proprietario=escambador)
        return produtos

class usuarioDao:
    def cadastrarUsuario(self, r, rfile):
        form = CadastroForm(r, rfile)
        if form.is_valid():
            return self.save(form.cleaned_data)   

    def save(self, cleaned_data):
        username = cleaned_data['username']
        password = cleaned_data['password1']
        cpf = cleaned_data['cpf']
        endereco = cleaned_data['endereco']
        telefone = cleaned_data['telefone']
        foto = cleaned_data['foto']

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
class escamboDao:
    def criar_escambo(self, cesta1 ,cesta2):
        escambo = Escambo()
        escambo.cestas.add(cesta1)
        escambo.cestas.add(cesta2)

        # Associa os usuários ao escambo
        escambo.usuarios.add(cesta1.escambador_dono)
        escambo.usuarios.add(cesta2.escambador_dono)
        
        # Salve o escambo no banco de dados
        escambo.save()
    
    def calcular_qnt_itens_escambo(self, escambo):
        for cesta in escambo.cestas.all():
            qnt_itens = cesta.produto.count()
        return qnt_itens
        
    def buscar_escambos_usuario(self, escambador):
        escambos = Escambo.objects.filter(usuarios=escambador)
        return escambos
    
    def todos_confirmados(self, escambo):
        return escambo.confirmado_usuario_iniciou and escambo.confirmado_usuario_outro


class categoriaDao:
    def buscarCategorias(self):
        return Categoria.objects.all()     
    
class genericaDao:
    def listarProdutosCategorias(self):        
        produtos = Produto.objects.exclude(status_trocado=True).order_by('-id')
        categorias = Categoria.objects.all()
        destaques = Produto.objects.filter(destaque=True).order_by('-id')
        
        context = { 
            'produtos': produtos,
            'categorias': categorias,
            'destaques': destaques
        }

        return context

class cestaDao:
    def calcular_qnt_itens_escambo(self, cesta):
        return cesta.produto.count()
