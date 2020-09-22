from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic.edit import CreateView
from django.views.generic import ListView

from .models import CustomUsuario
from django.urls import reverse_lazy

from .forms import CustomUsuarioCreationForm, LivroCreationForm, EditoraCreateForm, AutorCreationForm, EmprestimoLivroCreationForm

from .models import Livro, Categoria, Autor, Editora, Endereco, EmprestimoLivro

from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.utils import timezone


verificacao_campo_data_devolucao = None
verificacao_campo_quantidade = None
aux_instance_form = None

class IndexView(ListView):
    models = Livro
    template_name = 'livraria/home.html'
    queryset = Livro.objects.all()
    context_object_name = 'livros'


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
    #success_url = reverse_lazy('livraria:cadastrarautor')

    def get(self, request, *args, **kwargs):
        livro = Livro.objects.get(pk=self.kwargs['pk'])
        formEmprestimo = super(CreateEmprestimoLivro, self).get_form()

        context = {'formEmprestimo': formEmprestimo,
                   'livro': livro}
        
        return render(request, 'livraria/forms/emprestimo_livro.html',context)

    def post(self, request, *args, **kwargs):

        livro = Livro.objects.get(pk=self.kwargs['pk'])
        global verificacao_campo_data_devolucao
        global verificacao_campo_quantidade
        global aux_instance_form
        if verificacao_campo_data_devolucao == None and verificacao_campo_quantidade == None: 
            formEmprestimo = self.get_form()
            aux_instance_form = formEmprestimo
        else:
            formEmprestimo = aux_instance_form
      
        if formEmprestimo.is_valid():
            quantidade = formEmprestimo.cleaned_data['quantidade']
            data_inicial = formEmprestimo.cleaned_data['data_inicial']
            data_devolucao = formEmprestimo.cleaned_data['data_devolucao']
            preco_total = formEmprestimo.cleaned_data['preco']
            diferenca_data = data_devolucao - data_inicial

            
            if quantidade == 0:
                
                messages.error(request,'A quantidade não pode ser zero')

            elif quantidade > livro.estoque:
                messages.error(request,'A quantidade a ser emprestada, não pode ser maior que o estoque do livro')
            
            elif diferenca_data.days < 0:
                messages.error(request,'A data de devolução, não pode ser menor que a data inicio')
            
            else:
                calculo_emprestimo = livro.preco * quantidade
                print('Calculo emprestimo:', calculo_emprestimo)
                formEmprestimo.fields['preco'].initial = calculo_emprestimo



                livro.estoque = livro.estoque - quantidade
                
                if not verificacao_campo_quantidade == None and  not verificacao_campo_data_devolucao == None:
                    
                    if verificacao_campo_quantidade and verificacao_campo_data_devolucao:
                        emprestimo, created = EmprestimoLivro.objects.get_or_create(user=request.user,livro=livro, data_inicial=data_inicial, data_devolucao=data_devolucao, preco=calculo_emprestimo,ativo=True,quantidade=quantidade)
                       
                        livro.estoque = livro.estoque - quantidade
                        livro.preco_total = livro.preco * livro.estoque

                        livro.save()
                        emprestimo.save()
                        messages.success(request, 'Empréstimo realizado com sucesso!')
                else:
                    formEmprestimo.fields['data_devolucao'].widget.attrs['disabled'] = True
                    formEmprestimo.fields['quantidade'].widget.attrs['disabled'] = True

                    verificacao_campo_data_devolucao =  formEmprestimo.fields['data_devolucao'].widget.attrs['disabled']
                    print('Data devolucao:', verificacao_campo_data_devolucao)

                    verificacao_campo_quantidade = formEmprestimo.fields['quantidade'].widget.attrs['disabled']
                    
                    
                    


                   

        context = {'formEmprestimo': formEmprestimo,
                           'livro': livro
                    }
                  

        #if formEmprestimo.is_valid():
            #request.session['temp_data'] = livro
   
            
            #return render(request, 'livraria/forms/emprestimo_confirm.html', context)
            #return redirect('livraria:confirmaremprestimo')

        return render(request, 'livraria/forms/emprestimo_livro.html', context)




'''

from .forms import LivroForm, EditoraForm, EnderecoForm, AutorForm
from .models import Editora, Endereco, Autor, Livro, Categoria, EmprestimoLivro
from .forms import Livro_Emprestimo_Form, EmprestimoForm

from decimal import Decimal

#Variaveis globais
val_block = True
emprestimo_save = None

# Funções para realizar cadastros



# Mostrar listagem de livros
@login_required
def livraria_exibir_livros(request):

    list_Livros = Livro.objects.all().values()

    list_preco_total = []
    context= {
        'livros': Livro.objects.all(),
        'livros_preco_total':list_preco_total,
        'emprestimos':EmprestimoLivro.objects.all(),
    }

    return render(request,'produto/exibir_produtos.html',context)


@login_required
def livraria_detalhe_livro(request, pk):

    livro = get_object_or_404(Livro,id=pk)

    context = {
        'livro':livro,
    }

    return render(request,'produto/detalhe_produto.html', context)

@login_required
def livraria_editar_livro(request,pk):

    livro = get_object_or_404(Livro, pk=pk)
    
    formLivro = LivroForm(request.POST or None)
    formAutor = AutorForm(request.POST or None)

    if str(request.method) == 'POST':
        formLivro = LivroForm(request.POST, instance=livro)
        if formLivro.is_valid() and formAutor.is_valid():
                #livro = formLivro.save(commit=False)
 
            livro = formLivro.save(commit=False)
            livro.nome = formLivro.cleaned_data['nome']
            livro.preco = formLivro.cleaned_data['preco']
            livro.estoque = formLivro.cleaned_data['estoque']
            livro.num_paginas = formLivro.cleaned_data['num_paginas']
            livro.edicao = formLivro.cleaned_data['edicao']
            livro.descricao = formLivro.cleaned_data['descricao']
            livro.ano = formLivro.cleaned_data['ano']
            nomeAutor = formAutor.cleaned_data['nomeAutor']
            data_nascimento = formAutor.cleaned_data['ano']


            livro.preco_total = livro.estoque * livro.preco
            nomeCategoria = formLivro.cleaned_data['categorias']

            autor,created = Autor.objects.get_or_create(nome=nomeAutor, data_nascimento=data_nascimento)
            categoria, created = Categoria.objects.get_or_create(nome=nomeCategoria)
                
            livro.autor = autor
            livro.categoria = categoria
            livro.save()
                
            return redirect('livraria:livrariaexibirlivros')
    else:
        formLivro = LivroForm(instance=livro) 
        formAutor = AutorForm()

    context = {
        'formLivro':formLivro,
        'formAutor': formAutor,
    }

    return render(request,'forms/editar_produto.html',context)


@login_required
def livraria_deletar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    livro.delete()
    return redirect('livraria:livrariaexibirlivros')




@login_required
def livraria_realizar_emprestimo(request, pk):
    global val_block
    global emprestimo_save
    livro = get_object_or_404(Livro, pk=pk)
    form_livro = Livro_Emprestimo_Form(request.POST or None)
    form_emprestimo = EmprestimoForm(request.POST or None)
    calculo_final_emprestimo = 0   



    if str(request.method) == 'POST':
        if form_emprestimo.is_valid():
            data_inicial = form_emprestimo.cleaned_data['data_inicial']
            data_devolucao = form_emprestimo.cleaned_data['data_devolucao']
            quantidade = form_emprestimo.cleaned_data['quantidade']
            form_emprestimo.cleaned_data.get('preco')
            diferenca_data = data_devolucao - data_inicial


            if quantidade == 0:
                messages.error(request,'A quantidade não pode ser zero')

            elif quantidade > livro.estoque:
                messages.error(request,'A quantidade a ser emprestada, não pode ser maior que o estoque do livro')

            elif diferenca_data.days < 0:
                messages.error(request,'A data de devolução, não pode ser menor que a data inicio')
            elif not val_block:
                livro.estoque = livro.estoque -quantidade
                emprestimo_save.save()
                livro.save()
                emprestimo_save = None
                val_block = True
                return redirect('livraria:livrariaexibirlivros')
            else:
                calculo_Inicial_Emprestimo = Decimal(diferenca_data.days / 100)
                arrendondamento_calculo_emprestimo = round(calculo_Inicial_Emprestimo,2)
                calculo_final_emprestimo = livro.preco * arrendondamento_calculo_emprestimo
               
                if val_block:
                    emprestimo, created = EmprestimoLivro.objects.get_or_create(user=request.user,livro=livro, data_inicial=data_inicial, data_devolucao=data_devolucao, preco=calculo_final_emprestimo, ativo=True, quantidade=quantidade)
                    emprestimo_save = emprestimo
                    livro.estoque = livro.estoque -quantidade
                    val_block = False
            
                    
    else:
        form_livro = Livro_Emprestimo_Form(instance=livro)
        form_emprestimo = EmprestimoForm()
        messages.warning(request,'Atenção, voce precisa salvar para ser calculado o preço do empréstimo')
    
    form_emprestimo.fields['preco'].initial = calculo_final_emprestimo

    context = {
        'form_livro':form_livro,
        'form_emprestimo':form_emprestimo,
        'livro':livro,
    }
    
    return render(request, 'forms/emprestimo_livro.html', context)

@login_required
def livraria_devolver_livro(request, pk):

    emprestimo = get_object_or_404(EmprestimoLivro, pk=pk)
    livro = emprestimo.livro
    emprestimo.ativo = False
    livro.estoque = livro.estoque + emprestimo.quantidade
    emprestimo.quantidade = 0
    livro.save()
    emprestimo.save()
    return redirect('livraria:livrariaexibirlivros')

'''