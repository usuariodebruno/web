from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'escambo'

urlpatterns = [  

    # EscabadorView
    path('cadastroUsuario/', views.EscabadorView.cadastroUsuario, name='cadastro_usuario'), 
    path('', views.EscabadorView.index, name='index'),      
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),   

    # ProdutoView     
    path('cadastroProduto/', views.ProdutoView.cadastrar_produto, name='cadastrar_produto'), 
    path('pesquisar/', views.ProdutoView.pesquisar_produtos, name='pesquisar_produtos'),
    path('categoria/<int:categoria_id>/', views.ProdutoView.pesquisar_por_categoria, name='pesquisar_por_categoria'),
    path('detalheProduto/<int:produto_id>/', views.ProdutoView.detalhe_produto, name='detalhe_produto'),    
    path('meusProdutos/', views.ProdutoView.meus_produtos, name='meus_produtos'),    
    path('excluirProduto/<int:produto_id>', views.ProdutoView.excluir_produto, name='excluir_produto'),

    # CestaView   
    path('selecionarProdutos/<int:produto_id>/', views.CestaView.selecionar_produtos, name='selecionar_produtos'),

    # EscaboView    
    path('selecionarProdutosCesta/<int:produto_id>/', views.EscaboView.abrir_escambo, name='abrir_escambo'), 
    path('finalizarEscambo/<int:escambo_id>', views.EscaboView.finalizar_escambo, name='finalizar_escambo'),
    path('meusEscambos/', views.EscaboView.meus_escambos, name='meus_escambos'),   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)