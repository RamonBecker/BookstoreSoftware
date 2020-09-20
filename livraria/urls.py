from django.urls import path, include
from django.contrib.auth import views
from django.contrib import admin


#View
#from .views import livraria_base, #livraria_cadastrar_produto,livraria_cadastrar_editora
#from .views import livraria_exibir_livros, livraria_detalhe_livro , livraria_editar_livro, livraria_deletar_livro

#from .views import livraria_realizar_emprestimo, livraria_devolver_livro
from django.views.generic.base import TemplateView
from .views import SignUpView, CreateLivroView, CreateEditoraView, CreateAutorView

app_name = 'livraria'

urlpatterns = [
    path('', TemplateView.as_view(template_name='livraria/home.html'), name='home'),

    #Cadastros
    path('registrousuario', SignUpView.as_view(), name='registeruser'),
    path('cadastrolivro', CreateLivroView.as_view(),name='cadastrarlivro'),
    path('cadastroeditora', CreateEditoraView.as_view(), name='cadastrareditora'),
    path('cadastroautor', CreateAutorView.as_view(), name='cadastrarautor')
    #path('', livraria_base, name='home'),
    #Cadastros
    
   #path('/livraria_cadastrar_produto/', livraria_cadastrar_produto, name='livrariacadastrarproduto'),

    #path('/livraria_cadastrar_editora/', livraria_cadastrar_editora, name='livrariacadastrareditora'),

    #Exibição de livros cadastrados
    #path('/livraria_exibir_livros/', livraria_exibir_livros,name='livrariaexibirlivros'),

    #Detalhes do livros
    #path('/livraria_detalhe_livro/<int:pk>', livraria_detalhe_livro,name='livrariadetalhelivro'),

    #Editar livors
    #path('/livraria_editarlivro/<int:pk>',livraria_editar_livro, name='livrariaeditarlivro'),

    #Deletar livro
   # path('/livraria_deletarlivro/<int:pk>', livraria_deletar_livro, name='livrariadeletarlivro'),

    #Realizar emprestimo
    #path('/livraria_emprestimo_livro/<int:pk>', livraria_realizar_emprestimo, name='livrariaemprestimolivro'),

    #Devolver Livro
    ##path('/livraria_devolver_livro/<int:pk>',livraria_devolver_livro, name='livrariadevolverlivro')

]

