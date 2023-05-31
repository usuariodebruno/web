from django.contrib import admin
from .models import Usuario, Produto, Categoria, Troca

# Registro dos modelos no painel de administração
admin.site.register(Usuario)
admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Troca)
