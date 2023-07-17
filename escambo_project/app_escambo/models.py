from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Escambador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)      
    cpf = models.CharField(max_length=14, blank=True)          
    endereco = models.CharField(max_length=255)
    telefone = PhoneNumberField(blank=True)
    foto = models.ImageField(upload_to='escambo/usuario_fotos', null=True, blank=True)
    ativos = models.IntegerField(default=0)
    avaliacao = models.FloatField(default=5)    
    
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
    descricao_afetiva = models.CharField(max_length=500)
    estado_produto = models.CharField(max_length=20, choices=STATUS_CHOICES, default='bom')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    destaque = models.BooleanField(default=False)
    status_trocado = models.BooleanField(default=False)
    usuario_proprietario = models.ForeignKey(Escambador, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.nome

class Foto (models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='escambo/produto_fotos/', null=True, blank=True)

class Cesta(models.Model):   
    produto = models.ManyToManyField(Produto)
    obsvacoes = models.CharField(max_length=500, blank=True)    
    escambador_dono = models.ForeignKey(Escambador, on_delete=models.CASCADE)

    def calc_total_produtos(self):
        return self.produto.count()
    
    def __str__(self):
        return f"{self.id} - {self.escambador_dono.user.username} - {self.calc_total_produtos()} produtos"

class Chat(models.Model):    
    usuarios = models.ManyToManyField(Escambador)
    status_atividade = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Chat {self.id}'
    
class Mensagem(models.Model):    
    data_hora = models.DateTimeField(default=timezone.now)
    texto = models.CharField(max_length=2500)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)    
    remetente = models.ForeignKey(Escambador, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto
    
class Escambo(models.Model):
    usuarios = models.ManyToManyField(Escambador)     
    cestas = models.ManyToManyField(Cesta)    
    chat = models.ForeignKey(Chat, on_delete=models.SET_NULL , null=True) # !!!!!!!!!!!!!
    escambo_ativo = models.BooleanField(default=True)
    qnt_itens = models.IntegerField(default=0)
    usuario_iniciou = models.IntegerField(null=False, default=123)
    confirmado_usuario_iniciou = models.BooleanField(default=False)
    confirmado_usuario_outro = models.BooleanField(default=False)
  
    def __str__(self):
        #flat=True indica que queremos obter uma lista plana de valores, em vez de uma lista de tuplas.
        usernames = self.usuarios.values_list('user__username', flat=True) 
        return ' - '.join(usernames)
   