
from django.contrib.auth.models import User
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
    def criar_escambo(self, logado,  c1 ,c2):
        escambo = Escambo.objects.create(escambo_ativo=True, usuario_iniciou= logado.id) # Criar escambo

        escambo.cestas.add(c1, c2) # Adicionar as cestas ao escambo

        #dao = cestaDao()
        escambo.qnt_itens = (c1.produto.count()) + (c2.produto.count())

        escambo.usuarios.add(c1.escambador_dono, c2.escambador_dono)
        escambo.confirmado_usuario_iniciou = True
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

class cestaDao:
    def calcular_qnt_itens_escambo(self, cesta):
        return cesta.produto.count()

    def criar_cesta(self, escabador, produtos):
        cesta = Cesta.objects.create(escambador_dono=escabador) # Criar cesta

        if isinstance(produtos, list): # Verificar se produtos é uma lista 
            for p in produtos:
                cesta.produto.add(p)
            cesta.save()
        else:
            cesta.produto.add(produtos)
            cesta.save()

        return cesta 