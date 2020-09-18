from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from datetime import date
from django.utils import timezone

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from .models import CustomUsuario
from django.urls import reverse_lazy
from .forms import CustomUsuarioCreationForm
from sweetify.views import SweetifySuccessMixin



class SignUpView(SuccessMessageMixin,CreateView):
    form_class = CustomUsuarioCreationForm
    success_url = reverse_lazy('livraria:registeruser')
    template_name = 'livraria/register_user.html'
    success_message = 'Registro efetuado com sucesso'
    #def get_success_message(self, cleaned_data):
       # return 'Registro efetuado com sucesso'

'''

from .forms import LivroForm, EditoraForm, EnderecoForm, AutorForm
from .models import Editora, Endereco, Autor, Livro, Categoria, EmprestimoLivro
from .forms import Livro_Emprestimo_Form, EmprestimoForm

from decimal import Decimal

#Variaveis globais
val_block = True
emprestimo_save = None

@login_required
def livraria_base(request):

    context = {
        'livros':Livro.objects.all(),
    }

    return render(request, 'home.html', context)


# Funções para realizar cadastros
@login_required
def livraria_cadastrar_produto(request):

    form_Livro = LivroForm(request.POST or None)
    form_Autor = AutorForm(request.POST or None)
    
    invalid_Form = False

    
    if str(request.method) == 'POST':
        if form_Livro.is_valid() and form_Autor.is_valid():

            #Pegando dados do formulário de Livro
            nomeLivro = form_Livro.cleaned_data['nome']
            print(nomeLivro)
            preco = form_Livro.cleaned_data['preco']
            estoque = form_Livro.cleaned_data['estoque']
            edicao = form_Livro.cleaned_data['edicao']
            nome_categoria = form_Livro.cleaned_data['categorias']
            num_paginas = form_Livro.cleaned_data['num_paginas']
            descricao = form_Livro.cleaned_data['descricao']
            anoLivro = form_Livro.cleaned_data['ano']
            
                #Buscando editora selecionada

       

            idEditora = form_Livro.cleaned_data['editora']
            editora = Editora.objects.get(id=idEditora)

            #Pegando dados do formulario do autor
            nomeAutor = form_Autor.cleaned_data['nomeAutor']
            data_nascimento = form_Autor.cleaned_data['ano']
                
            #Pegando categoria do bd, se não encontrar cria uma nova categoria

            categoria,created =  Categoria.objects.get_or_create(nome=nome_categoria)              

            #Pegando autor do bd, se não encontrar cria um autor
            autor,created = Autor.objects.get_or_create(nome=nomeAutor, data_nascimento=data_nascimento)

            #Pega o livro do bd, se não encontrar cria um livro novo
            livro, created = Livro.objects.get_or_create(nome=nomeLivro,preco=preco,estoque=estoque,edicao=edicao,num_paginas=num_paginas,descricao=descricao, ano=anoLivro, autor=autor,editora=editora, categoria=categoria)
            livro.preco_total = estoque * preco
            livro.save()
            messages.success(request,'Livro cadastrado com sucesso !')
            form_Livro = LivroForm()
            form_Autor = AutorForm()

    messages.warning(request,'Atenção, voce precisa cadastrar pelo menos uma editora para cadastrar o livro')

    context = {
        'formLivro': form_Livro,
        'formAutor': form_Autor
    }
    

    return render(request, 'forms/add_livro.html', context)

@login_required
def livraria_cadastrar_editora(request):

    aux_Editora_form = EditoraForm(request.POST or None)
    aux_Endereco_form = EnderecoForm(request.POST or None)

    invalid_Form = False

    if str(request.method) == 'POST':
        if aux_Editora_form.is_valid() and aux_Endereco_form.is_valid():
            
            rua = aux_Endereco_form.cleaned_data['rua']
            bairro = aux_Endereco_form.cleaned_data['bairro']
            cidade = aux_Endereco_form.cleaned_data['cidade']
            estado = aux_Endereco_form.cleaned_data['estado']
            numero = aux_Endereco_form.cleaned_data['numero']
            nomeEditora = aux_Editora_form.cleaned_data['nome']

            endereco,created = Endereco.objects.get_or_create(rua=rua, bairro=bairro, cidade=cidade, estado=estado, numero=numero)
            editora, created = Editora.objects.get_or_create(nome=nomeEditora, endereco=endereco)
            editora.save()
            messages.success(request,'Editora cadastrada com sucesso !')
    
  
    aux_Editora_form = EditoraForm()
    aux_Endereco_form = EnderecoForm()

    context = {
         'editoraForm':aux_Editora_form,
         'enderecoForm': aux_Endereco_form,
    }

    return render(request, 'forms/add_editora.html', context)


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