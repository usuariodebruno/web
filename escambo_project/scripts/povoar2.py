""""
    POVOAR APLICAÇÃO COM ESCABADORES, PRODUTOS E SUAS FOTOS
    Navegue até a pasta do projeto django, onde está o arquivo manage.py e abra o modo interatiivo shell do python executando o comando: 
    $ python manage.py shell

    Dentro do Shell, execute o comando para rodar:
    >>> exec(open('scripts/povoar2.py').read())
    
"""
import random
from django.contrib.auth.models import User
from faker import Faker
from app_escambo.models import Escambador, Cesta, Chat, Escambo, Produto, Categoria, Mensagem

fake = Faker()

def create_cestas_escambos():
    escambadores = Escambador.objects.all()

    for _ in range(10):
        # Selecionar 2 escambadores aleatoriamente
        escambadores_participantes = random.sample(list(escambadores), 2)

        # Criar chat com os escambadores participantes
        chat = Chat.objects.create(status_atividade=True)
        chat.usuarios.set(escambadores_participantes)

        # Criar escambo com o chat e os escambadores participantes
        escambo = Escambo.objects.create(chat=chat, status_escambo=True)
        escambo.usuarios.set(escambadores_participantes)

        for _ in range(2):
            # Criar cesta
            cesta = Cesta.objects.create(obsvacoes=fake.text(max_nb_chars=500), escambador_dono=random.choice(escambadores_participantes))

            # Adicionar 10 produtos à cesta
            for _ in range(10):
                nome_produto = fake.sentence(nb_words=3, variable_nb_words=True)
                descricao_afetiva = fake.sentence()
                estado_produto = random.choice(['ruim', 'ok', 'bom', 'ótimo', 'excelente'])
                categoria = random.choice(Categoria.objects.all())
                usuario_proprietario = random.choice(escambadores_participantes)

                produto = Produto.objects.create(nome=nome_produto, descricao_afetiva=descricao_afetiva, estado_produto=estado_produto, categoria=categoria, usuario_proprietario=usuario_proprietario)
                cesta.produto.add(produto)

            # Associar cesta ao escambo
            escambo.cestas.add(cesta)

            # Criar mensagens para o chat
            for _ in range(5):
                texto_mensagem = fake.text(max_nb_chars=230)
                remetente = random.choice(escambadores_participantes)
                mensagem = Mensagem.objects.create(texto=texto_mensagem, chat=chat, remetente=remetente)

create_cestas_escambos()
print("######### CRIAR ESCAMBO #########")
print("-CESTAS CRIADAS \n-PRODUTOS ADICIONADOS A CESTA \n-CHATS E PARTICIPANTES DE CESTAS CRIADOS \n-CHATS DE CESTAS CRIADOS \n   - mensanges de chat criadas")