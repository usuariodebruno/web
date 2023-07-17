from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


app_name = 'escambo'

urlpatterns = [    
    path('', views.index, name='index'),
    path('cadastroUsuario/', views.cadastroUsuario, name='cadastro_usuario'),        
    path('cadastroProduto/', views.cadastrar_produto, name='cadastrar_produto'), 
    path('pesquisar/', views.pesquisar_produtos, name='pesquisar_produtos'),
    path('categoria/<int:categoria_id>/', views.pesquisar_por_categoria, name='pesquisar_por_categoria'),
    path('detalheProduto/<int:produto_id>/', views.detalhe_produto, name='detalhe_produto'),
    path('selecionarProdutosCesta/<int:produto_id>/', views.selecionar_produtos_cesta, name='selecionar_produtos_cesta'),    
    path('selecionarTeste/<int:produto_id>/', views.selecionar_produtos_teste, name='selecionar_produtos_teste'),
    path('excluirProduto/<int:produto_id>', views.excluir_produto, name='excluir_produto'),
    path('finalizarEscambo/<int:escambo_id>', views.finalizar_escambo, name='finalizar_escambo'),
    path('meusEscambos/', views.meus_escambos, name='meus_escambos'),    
    path('meusProdutos/', views.meus_produtos, name='meus_produtos'),
    path('teste/', views.teste, name='teste'),

 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)