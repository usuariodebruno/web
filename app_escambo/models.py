from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from pytz import timezone

class Termos(models.Model):
    status_termo = models.BooleanField(default=False)
    pdf_file = models.FileField(upload_to='pdfs/')
    class Meta:
        verbose_name_plural = 'Termos'

    def __str__(self):
        return str(self.pdf_file)

class Escambador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)      
    cpf = models.CharField(max_length=14, blank=True)          
    endereco = models.CharField('Endereço', max_length=255)
    telefone = PhoneNumberField(blank=True)
    foto = models.ImageField(upload_to='usuario_fotos/', null=True, blank=True)
    avaliacao = models.FloatField('Avaliação', default=5)    

    termos = models.ForeignKey(Termos, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Escambadores'

    def __str__(self):
        return self.user.username
      

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    STATUS_CHOICES = (
        ('ruim', 'Ruim'),
        ('ok', 'Ok'),
        ('bom', 'Bom'),
        ('ótimo', 'Ótimo'),
        ('excelente', 'Excelente'),
    )

    nome = models.CharField(max_length=100)
    descricao_afetiva = models.TextField()
    foto = models.ImageField(upload_to='media/', null=True, blank=True)
    estado_produto = models.CharField(max_length=20, choices=STATUS_CHOICES, default='bom')

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    usuario_proprietario = models.ForeignKey(Escambador, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Escambo(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('concluida', 'Concluída'),
    )

    produto1 = models.ForeignKey(Produto, related_name='trocas1', on_delete=models.CASCADE)
    produto2 = models.ForeignKey(Produto, related_name='trocas2', on_delete=models.CASCADE)
    usuario1 = models.ForeignKey(Escambador, related_name='trocas1', on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(Escambador, related_name='trocas2', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return "status: " +self.status


class Chat(models.Model):
    status_atividade = models.BooleanField(default=False)
    participantes = models.ManyToManyField(Escambador, blank=True)
    
    def __str__(self):
        return f'Chat {self.id}'
    
class Mensagem(models.Model):    
    data_hora = models.DateTimeField(default=datetime.now(timezone('America/Sao_Paulo')), blank=True, )
    texto = models.CharField(max_length=2500)

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    def __str__(self):
        return self.texto