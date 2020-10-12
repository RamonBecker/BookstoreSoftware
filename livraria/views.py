from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView

from django.urls import reverse_lazy

from .forms import CustomUsuarioCreationForm, CustomUsuarioChangeForm ,LivroCreationForm, EditoraCreateForm, AutorCreationForm, EmprestimoLivroCreationForm

from .models import Livro, Categoria, Autor, Editora, Endereco, EmprestimoLivro, CustomUsuario

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.forms import PasswordChangeForm



# ----------- Variáveis globais ------------

verificacao_campo_data_devolucao = None
verificacao_campo_quantidade = None
aux_instance_form = None
verificacao_botao_salvar = True




# ----------- DeleteView ------------

class DeleteLivroView(DeleteView):
    model = Livro
    template_name = 'livraria/forms/livro_confirm_delet.html'
    success_url = reverse_lazy('livraria:listarlivros')
    success_message = 'Livro deletado com sucesso!'


# ----------- DetailView ------------

class LivrosDetailView(DetailView):
     model = Livro
    #queryset = Livro.objects.all()
     template_name = 'livraria/produto/detalhe_livro.html'

    #def get(self, request, *args, **kwargs):
     #   livro = get_object_or_404(Livro, pk=kwargs['pk'])
      #  context = {'livro': livro}
      #  return render(request, 'livraria/produto/detalhe_livro.html', context)
   # def get_object(self):
     #  id_ = self.kwargs.get("id")
      #  return get_object_or_404(Livro, id=id_)

# ----------- ListView ------------

class LivrosListView(ListView):
    model = Livro
    template_name = 'livraria/produto/exibir_livros.html'
    queryset = Livro.objects.all()
    context_object_name = 'livros'


class ListEmprestimosView(ListView):
    model = EmprestimoLivro
    template_name = 'livraria/produto/exibir_emprestimos.html'
    queryset = EmprestimoLivro.objects.all()
    context_object_name = 'emprestimos'


class IndexView(ListView):
    models = Livro
    template_name = 'livraria/home.html'
    queryset = Livro.objects.all()
    context_object_name = 'livros'


# ----------- CreateView ------------

class SignUpView(SuccessMessageMixin,CreateView):
    form_class = CustomUsuarioCreationForm
    success_url = reverse_lazy('livraria:registeruser')
    template_name = 'livraria/register_user.html'
    success_message = 'Cadastro efetuado com sucesso!'


class CreateLivroView(LoginRequiredMixin, SuccessMessageMixin,CreateView):
    login_url = 'login'
    redirect_field_name = 'login'
    form_class = LivroCreationForm
    success_url = reverse_lazy('livraria:cadastrarlivro')
    template_name = 'livraria/forms/add_livro.html'

    def get(self, request, *args, **kwargs):
        autores = Autor.objects.all()
        editoras = Editora.objects.all()
        formLivro = super(CreateLivroView, self).get_form()
        context = {'formLivro': formLivro,
                   'autores': autores,
                   'editoras': editoras}
        return render(request, 'livraria/forms/add_livro.html',context)

    def post(self, request, *args, **kwargs):
        formLivro = self.get_form()
        autores = Autor.objects.all()
        editoras = Editora.objects.all()


        if formLivro.is_valid():
            nome = formLivro.cleaned_data['nome']
            preco = formLivro.cleaned_data['preco']
            estoque = formLivro.cleaned_data['estoque'] 
            edicao = formLivro.cleaned_data['edicao']
            ano = formLivro.cleaned_data['ano']
            num_paginas = formLivro.cleaned_data['num_paginas']
            descricao = formLivro.cleaned_data['descricao']

            editora = formLivro.cleaned_data['editora']
            autor = formLivro.cleaned_data['autor'] 
            categoria = formLivro.cleaned_data['categoria']


            print(formLivro.cleaned_data)
            if estoque <= 0:
                messages.error(request,'O estoque não pode ser zero ou negativo')

            elif num_paginas <= 0:
                messages.error(request,'O número de páginas não pode ser zero ou negativo')

            else:

                aux_editora, created = Editora.objects.get_or_create(id=editora.id)
                aux_autor, created = Autor.objects.get_or_create(id=autor.id)
                aux_categoria, created = Categoria.objects.get_or_create(nome=categoria)
            
                preco_total = preco * estoque
                
                livro, created = Livro.objects.get_or_create(nome=nome, preco=preco, estoque=estoque, edicao=edicao, ano=ano, num_paginas=num_paginas, descricao=descricao, editora=aux_editora, autor=aux_autor, categoria=aux_categoria, preco_total=preco_total)

                messages.success(request,'Cadastro realizado com sucesso!')
                livro.save()
                
                formLivro = LivroCreationForm()


        context = {'formLivro': formLivro,
                   'editoras': editoras,
                   'autores': autores
                  }

        return render(request, 'livraria/forms/add_livro.html' , context)


class CreateEditoraView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'login'
    model = Editora
    form_class = EditoraCreateForm
    success_url = reverse_lazy('livraria:cadastrareditora')

    def get(self, request, *args, **kwargs):
        form = super(CreateEditoraView, self).get_form()
        context = {'formEditora': form}
        return render(request, 'livraria/forms/add_editora.html', context)

    def post(self, request, *args, **kwargs):
        formEditora = self.get_form()

        if formEditora.is_valid():

            rua = formEditora.cleaned_data['rua']
            bairro = formEditora.cleaned_data['bairro']
            cidade = formEditora.cleaned_data['cidade']
            estado = formEditora.cleaned_data['estado']
            numero = formEditora.cleaned_data['numero']
            nomeEditora = formEditora.cleaned_data['nome']

            endereco, created = Endereco.objects.get_or_create(rua=rua, bairro=bairro, numero=numero, cidade=cidade, estado=estado)
            editora, created = Editora.objects.get_or_create(nome=nomeEditora, endereco=endereco)
            messages.success(request,'Cadastro realizado com sucesso!')
            editora.save()

        formEditora = EditoraCreateForm()

        return render(request, 'livraria/forms/add_editora.html', {'formEditora': formEditora})


class CreateAutorView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'login'
    form_class = AutorCreationForm
    template_name = 'livraria/forms/add_autor.html'
    success_url = reverse_lazy('livraria:cadastrarautor')

    def get(self, request, *args, **kwargs):
        formAutor = super(CreateAutorView, self).get_form()
        context = {'formAutor': formAutor}
        return render(request, 'livraria/forms/add_autor.html',context)

    def post(self, request, *args, **kwargs):
        formAutor = self.get_form()

        if formAutor.is_valid():

            nome = formAutor.cleaned_data['nome']
            data_nascimento = formAutor.cleaned_data['data_nascimento']
            print('data nascimento:', data_nascimento)
            autor, created = Autor.objects.get_or_create(nome=nome, data_nascimento=data_nascimento)
            messages.success(request,'Cadastro realizado com sucesso!')
            autor.save()

        formAutor = AutorCreationForm()
        

        return render(request, 'livraria/forms/add_autor.html' , {'formAutor': formAutor})


class CreateEmprestimoLivro(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'login'
    form_class = EmprestimoLivroCreationForm
    template_name = 'livraria/forms/emprestimo_livro.html'

    def get(self, request, *args, **kwargs):
        livro = Livro.objects.get(pk=self.kwargs['pk'])
        formEmprestimo = super(CreateEmprestimoLivro, self).get_form()
        global verificacao_botao_salvar
        #aux_instance_form = formEmprestimo


        context = {'formEmprestimo': formEmprestimo,
                   'livro': livro, 
                   'verificacao_botao_salvar':verificacao_botao_salvar
                   }
        
        return render(request, 'livraria/forms/emprestimo_livro.html',context)

    def post(self, request, *args, **kwargs):

        livro = Livro.objects.get(pk=self.kwargs['pk'])
        global verificacao_campo_data_devolucao
        global verificacao_campo_quantidade
        global aux_instance_form
        global verificacao_botao_salvar

        if verificacao_campo_data_devolucao == None and verificacao_campo_quantidade == None: 
            formEmprestimo = self.get_form()
            aux_instance_form = formEmprestimo
           # print('FORM emprestimo:', formEmprestimo)
            print('CAiu na verificação da data')
        else:
            print('CAiu no else')
            formEmprestimo = aux_instance_form
      
        if formEmprestimo.is_valid():
            quantidade = formEmprestimo.cleaned_data['quantidade']
            data_inicial = formEmprestimo.cleaned_data['data_inicial']
            data_devolucao = formEmprestimo.cleaned_data['data_devolucao']
            preco_total = formEmprestimo.cleaned_data['preco']
            diferenca_data = data_devolucao - data_inicial

            print('DATA INCIAL', data_inicial)
            print('DATA DEVOULAÇÂO:', data_devolucao)
            print('DIFERENÇA', diferenca_data.days)
            if quantidade == 0:
                
                messages.error(request,'A quantidade não pode ser zero')

            elif quantidade > livro.estoque:
                messages.error(request,'A quantidade a ser emprestada, não pode ser maior que o estoque do livro')
            
            elif diferenca_data.days < 0:
                messages.error(request,'A data de devolução, não pode ser menor que a data inicio')
            
            else:
                calculo_emprestimo = livro.preco * quantidade
                formEmprestimo.fields['preco'].initial = calculo_emprestimo

                livro.estoque = livro.estoque - quantidade

                if not verificacao_campo_quantidade == None and  not verificacao_campo_data_devolucao == None:
                    
                    if verificacao_campo_quantidade and verificacao_campo_data_devolucao:
                        
                        emprestimo = EmprestimoLivro.objects.create(user=request.user,livro=livro, data_inicial=data_inicial, data_devolucao=data_devolucao, preco=calculo_emprestimo,ativo=True,quantidade=quantidade)

                        livro.preco_total = livro.preco_total - calculo_emprestimo
                       
                       
                        #verificacao_botao_confirmar = False
                        verificacao_botao_salvar = False
                        
                        livro.save()
                        emprestimo.save()
                        messages.success(request, 'Empréstimo realizado com sucesso!')
                        verificacao_campo_quantidade = None
                        verificacao_campo_data_devolucao = None
                        #aux_instance_form = formEmprestimo
                        #
                else:
                    formEmprestimo.fields['data_devolucao'].widget.attrs['disabled'] = True
                    formEmprestimo.fields['quantidade'].widget.attrs['disabled'] = True

                    verificacao_campo_data_devolucao =  formEmprestimo.fields['data_devolucao'].widget.attrs['disabled']
                    print('Data devolucao:', verificacao_campo_data_devolucao)

                    verificacao_campo_quantidade = formEmprestimo.fields['quantidade'].widget.attrs['disabled']
                    #   

        context = {'formEmprestimo': formEmprestimo,
                    'livro': livro,
                    'verificacao_botao_salvar':verificacao_botao_salvar
                    }
        verificacao_botao_salvar = True
    
        return render(request, 'livraria/forms/emprestimo_livro.html', context)


# ----------- UpdateView ------------
class UpdateLivroView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request, *args, **kwargs):
        livro = Livro.objects.get(pk=self.kwargs['pk'])
        formLivro = LivroCreationForm(instance=livro)
        context = {'formLivro': formLivro,}
        return render(request, 'livraria/forms/editar_livro.html', context)

    def post(self, request, *args, **kwargs):
        livro = Livro.objects.get(pk=self.kwargs['pk'])
        formLivro = LivroCreationForm(request.POST or None)

        if formLivro.is_valid():


            preco = formLivro.cleaned_data['preco']
            estoque = formLivro.cleaned_data['estoque']

            livro.nome = formLivro.cleaned_data['nome']
            livro.preco = formLivro.cleaned_data['preco']
            livro.estoque = formLivro.cleaned_data['estoque'] 
            livro.edicao = formLivro.cleaned_data['edicao']
            livro.ano = formLivro.cleaned_data['ano']
            livro.num_paginas = formLivro.cleaned_data['num_paginas']
            livro.descricao = formLivro.cleaned_data['descricao']

            editora = formLivro.cleaned_data['editora']
            autor = formLivro.cleaned_data['autor']
            categoria = formLivro.cleaned_data['categoria']
          

            if livro.estoque <= 0:
                messages.error(request,'O estoque não pode ser zero ou negativo')

            elif livro.num_paginas <= 0:
                messages.error(request,'O número de páginas não pode ser zero ou negativo')

            elif livro.preco <= 0:
                messages.error(request,'O preço não pode ser zero ou negativo')

            else:

                aux_editora, created = Editora.objects.get_or_create(id=editora.id)
                aux_autor, created = Autor.objects.get_or_create(id=autor.id)
                aux_categoria, created = Categoria.objects.get_or_create(nome=categoria)
            
                livro.preco_total = preco * estoque
                livro.editora = aux_editora
                livro.autor = aux_autor
                livro.categoria = aux_categoria

                messages.success(request,'Cadastro realizado com sucesso!')
                livro.save()
                
                formLivro = LivroCreationForm()
                return redirect('livraria:listarlivros')



        context = {'formLivro': formLivro,}
 
        return render(request, 'livraria/forms/editar_livro.html', context)


class UpdateEmprestimoView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request, *args, **kwargs):
        emprestimo = EmprestimoLivro.objects.get(pk=self.kwargs['pk'])
        emprestimo.ativo = False
        livro = emprestimo.livro
        livro.estoque = livro.estoque + emprestimo.quantidade
        aux_preco_total = emprestimo.quantidade * emprestimo.preco
        livro.preco_total += aux_preco_total
        emprestimo.quantidade = 0
        livro.save()
        emprestimo.save()
        messages.success(request,'Livro devolvido com sucesso!')

        return redirect('livraria:listaremprestimos')

 
class ProfileUserView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    template_name = 'profile.html'


class UpdateUserView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    login_url = 'login'
    redirect_field_name = 'login'
    model = CustomUsuario
    form_class = CustomUsuarioChangeForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('livraria:profileuser')
    success_message = 'Dados atualizados com sucesso!'