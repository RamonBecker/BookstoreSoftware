from django.urls import path, include
from django.conf.urls import url

from django.contrib.auth import views
from django.contrib import admin


from django.views.generic.base import TemplateView
from .views import SignUpView, CreateLivroView, CreateEditoraView, CreateAutorView,IndexView, CreateEmprestimoLivro, LivrosListView, LivrosDetailView

app_name = 'livraria'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),

    #Cadastros
    path('registrousuario', SignUpView.as_view(), name='registeruser'),
    path('cadastrolivro', CreateLivroView.as_view(),name='cadastrarlivro'),
    path('cadastroeditora', CreateEditoraView.as_view(), name='cadastrareditora'),
    path('cadastroautor', CreateAutorView.as_view(), name='cadastrarautor'),

    #Emprestimo
    path('<int:pk>/emprestimolivro/', CreateEmprestimoLivro.as_view(), name='emprestarlivro'),
    #Exibição de livros
    path('exibirlivros', LivrosListView.as_view(), name='listarlivros'),
    #re_path(r'(?P<pk>[0-9]+)detalhelivro$', LivrosDetailView.as_view(), name='detaillivro'),
   # path('<int:pk>/detalhelivro', LivrosDetailView.as_view(), name='detaillivro'),
    url(r'^detalhelivro/(?P<pk>[0-9]+)/$', LivrosDetailView.as_view(), name='detaillivro')
    #Detalhes do livros
    #path('/livraria_detalhe_livro/<int:pk>', livraria_detalhe_livro,name='livrariadetalhelivro'),

    #Editar livors
    #path('/livraria_editarlivro/<int:pk>',livraria_editar_livro, name='livrariaeditarlivro'),

    #Deletar livro
   # path('/livraria_deletarlivro/<int:pk>', livraria_deletar_livro, name='livrariadeletarlivro'),


    #Devolver Livro
    ##path('/livraria_devolver_livro/<int:pk>',livraria_devolver_livro, name='livrariadevolverlivro')

]

