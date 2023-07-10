from django.contrib import admin
from .models import *

# Registro dos modelos no painel de administração
admin.site.register(Termos)
admin.site.register(Escambador)
admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Escambo)
admin.site.register(Chat)
admin.site.register(Mensagem)
