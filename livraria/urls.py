from django.urls import path, include
from django.conf.urls import url

from django.contrib.auth import views
from django.contrib import admin


from django.views.generic.base import TemplateView
from .views import SignUpView, IndexView ,CreateLivroView, CreateEditoraView, CreateAutorView,CreateEmprestimoLivro, ListEmprestimosView, UpdateEmprestimoView, LivrosListView,LivrosDetailView, UpdateLivroView, DeleteLivroView, ProfileUserView, UpdateUserView

from django.contrib.auth import views as auth_views

app_name = 'livraria'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),

    url(r'^atualizarconta/(?P<pk>[0-9]+)/$', UpdateUserView.as_view(), name='updateuser'),
    path('minhaconta', ProfileUserView.as_view(), name='profileuser'),
    #Cadastros
    path('registrousuario', SignUpView.as_view(), name='registeruser'),
    path('cadastrolivro', CreateLivroView.as_view(),name='cadastrarlivro'),
    path('cadastroeditora', CreateEditoraView.as_view(), name='cadastrareditora'),
    path('cadastroautor', CreateAutorView.as_view(), name='cadastrarautor'),

    #Emprestimo
    path('<int:pk>/emprestimolivro/', CreateEmprestimoLivro.as_view(), name='emprestarlivro'),

    path('exibiremprestimos', ListEmprestimosView.as_view(), name='listaremprestimos'),

    #path('<int>:pk/devolucaolivro/', UpdateEmprestimoView.as_view(), name='devolverlivro'),

     url(r'^devolucaolivro/(?P<pk>[0-9]+)/$', UpdateEmprestimoView.as_view(), name='devolverlivro'),

    #Exibição de livros
    path('exibirlivros', LivrosListView.as_view(), name='listarlivros'),

    #detalhe
    url(r'^detalhelivro/(?P<pk>[0-9]+)/$', LivrosDetailView.as_view(), name='detaillivro'),

    #Editar

    url(r'^edicaolivro/(?P<pk>[0-9]+)/$', UpdateLivroView.as_view(), name='editarlivro'),

    #excluir livro
    path('<int:pk>deletarlivro', DeleteLivroView.as_view(), name='deletelivro'),

    #Devolver Livro
    ##path('/livraria_devolver_livro/<int:pk>',livraria_devolver_livro, name='livrariadevolverlivro')

]

