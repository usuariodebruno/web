from django.contrib import messages
from django import forms
from .models import *
from .forms import *
    
class produtoDao:
    def cadastrarProduto(self, r, rfile):
        form = ProdutoForm(r, rfile)
        if form.is_valid():
            return self.save(form.cleaned_data)

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

class genericaDao:
    def listarProdutosCategorias(self):        
        produtos = Produto.objects.all().order_by('-id')
        categorias = Categoria.objects.all() 
        
        context = { 
            'produtos': produtos,
            'categorias': categorias,
        }

        return context