from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'escambo'

urlpatterns = [    
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),        
    path('cadastroProduto/', views.cadastrar_produto, name='cadastrar_produto'), 
    path('pesquisar/', views.pesquisar_produtos, name='pesquisar_produtos'),
    path('categoria/<int:categoria_id>/', views.pesquisar_por_categoria, name='pesquisar_por_categoria'),

    # URL de login
    path('login/', auth_views.LoginView.as_view(template_name='escambo/login.html'), name='login'),
    path('autenticado/', views.login_view, name='autenticado'),

    # URL de logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)