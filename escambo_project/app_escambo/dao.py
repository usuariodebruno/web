from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from .models import *
from .forms import *
    
class produtoDao:
    def cadastrarProduto(self, r, rfile):
        form = ProdutoForm(r, rfile)
        if form.is_valid():
            return self.save(form.cleaned_data)
    
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
    
    def save(self, cleaned_data):
        nome = cleaned_data['nome']
        descricao_afetiva = cleaned_data['descricao_afetiva']
        estado_produto = cleaned_data['estado_produto']
        categoria = cleaned_data['categoria']
        usuario_proprietario = cleaned_data['usuario_proprietario']

        produto = Produto.objects.create(
            nome=nome,
            descricao_afetiva=descricao_afetiva,
            estado_produto=estado_produto,
            categoria=categoria,
            usuario_proprietario=usuario_proprietario
        )

        for image in cleaned_data['fotos']:
            Foto.objects.create(produto=produto, imagem=image)

        return produto

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

class categoriaDao:
    def buscarCategorias(self):
        return Categoria.objects.all()     
    
class genericaDao:
    def listarProdutosCategorias(self):        
        produtos = Produto.objects.all().order_by('-id')
        categorias = Categoria.objects.all() 
        
        context = { 
            'produtos': produtos,
            'categorias': categorias,
        }

        return context

"""
class loginDao:
    def login(self, r):
        form = LoginForm(r, data=r.POST)        
        if form.is_valid():
            nome = form.cleaned_data['username']
            senha = form.cleaned_data['password']
            user = authenticate(request=r, username=nome, password=senha)
            if user is not None:
                return user
        else:        
            mensagem = messages.get_messages(r)
            form = LoginForm()   
            context = {
                'mensagem': messages.error(r, 'Credenciais inválidas. Por favor, tente novamente.'),
                'form': form
            }
            return context 
                       
    def pegarFormularioLimpo(self):
        return LoginForm()
    
    def pegarFormularioSessao(self, r):
        return LoginForm(r, data=r.POST)
"""