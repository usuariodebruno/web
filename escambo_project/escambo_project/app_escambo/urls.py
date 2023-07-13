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

 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)