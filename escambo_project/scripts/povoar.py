""""
    POVOAR APLICAÇÃO COM ESCABADORES, PRODUTOS E SUAS FOTOS
    Navegue até a pasta do projeto django, onde está o arquivo manage.py e abra o modo interatiivo shell do python executando o comando: 
    $ python manage.py shell

    Dentro do Shell, execute o comando para rodar:
    >>> exec(open('scripts/povoar.py').read())
    
"""
from django.contrib.auth.models import User
from faker import Faker
from app_escambo.models import Escambador, Produto, Foto, Categoria
import random

fake = Faker()

def create_escambadores():
    for _ in range(5):
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        user = User.objects.create_user(username=username, password=password, email=email)

        cpf = fake.random_int(min=10000000000, max=99999999999)
        endereco = fake.address()
        telefone = fake.phone_number()
        foto = None  # Preencha com o caminho da imagem se desejar
        avaliacao = fake.pyfloat(min_value=0, max_value=5)

        escambador = Escambador.objects.create(user=user, cpf=cpf, endereco=endereco, telefone=telefone, foto=foto, avaliacao=avaliacao)

        create_produtos(escambador)

def create_produtos(escambador):
    for _ in range(40):
        nome = fake.word()
        descricao_afetiva = fake.text(max_nb_chars=500)
        estado_produto = fake.random_element(elements=('ruim', 'ok', 'bom', 'ótimo', 'excelente'))
        categoria = Categoria.objects.get(id= (random.randint(1 ,4 )))
        produto = Produto.objects.create(nome=nome, descricao_afetiva=descricao_afetiva, estado_produto=estado_produto, categoria=categoria, usuario_proprietario=escambador)

        #create_fotos(produto)
'''
def create_fotos(produto):
    for _ in range(3):
        imagem = '/static/escambo/img/produto/produto_padrao_foto.png'  # Preencha com o caminho da imagem se desejar
        foto = Foto.objects.create(produto=produto, imagem=imagem)
'''
create_escambadores()

print("-ESCAMBADORES CRIADOS \n-RODUTOS CRIADOS \n   - fotos para produtos criada")

