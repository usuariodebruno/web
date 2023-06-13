from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)      
    cpf = models.CharField(max_length=14)          
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='usuario_fotos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='media/', null=True, blank=True)
    usuario_proprietario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Troca(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('concluida', 'Concluída'),
    )

    produto1 = models.ForeignKey(Produto, related_name='trocas1', on_delete=models.CASCADE)
    produto2 = models.ForeignKey(Produto, related_name='trocas2', on_delete=models.CASCADE)
    usuario1 = models.ForeignKey(User, related_name='trocas1', on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(User, related_name='trocas2', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f'Troca {self.id}'


class Chat(models.Model):
    participantes = models.ManyToManyField(User)
    mensagens = models.TextField()

    def __str__(self):
        return f'Chat {self.id}'
