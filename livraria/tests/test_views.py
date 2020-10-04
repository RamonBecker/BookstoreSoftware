from django.test import TestCase
from django.test import Client
from django.test import RequestFactory
from django.urls import reverse_lazy
from django.urls import reverse
from model_mommy import mommy

from livraria.forms import AutorCreationForm, EditoraCreateForm, EmprestimoLivroCreationForm
from livraria.models import Autor, Editora, Livro, Categoria, Endereco, EmprestimoLivro

class IndexViewTestCase(TestCase):

    def setUp(self):
        self.cliente = Client()
        self.livro1 = mommy.make('Livro')
        self.livro2 = mommy.make('Livro')
        self.livro3 = mommy.make('Livro')
        self.livro4 = mommy.make('Livro')
        self.livro5 = mommy.make('Livro')

        self.livro1.save()
        self.livro2.save()
        self.livro3.save()
        self.livro4.save()
        self.livro5.save()
        
    def test_list_view(self):
     
        livros = Livro.objects.all()
        request = self.client.get(reverse_lazy('livraria:home'), context={'livros':livros})

        self.assertEquals(request.status_code, 200)
        self.assertQuerysetEqual(list(request.context['livros']), livros,  transform=lambda x: x)


class CreateAutorViewTestCase(TestCase):

    def setUp(self):

        
        self.dados = {
            'nome':'Teste Nome',
            'data_nascimento':'2020-01-01'
        }
        self.form = AutorCreationForm(data=self.dados)
        self.cliente = Client()


    def test_GET(self):
        request = self.cliente.get(reverse_lazy('livraria:cadastrarautor'), data={'formAutor': self.form})
        self.assertEquals(request.status_code, 302)

    def test_POST(self):

        request = self.client.post(reverse_lazy('livraria:cadastrarautor'), {'form':self.form})

        self.assertEquals(request.status_code, 302)
        self.assertTrue(self.form.is_valid())

        if self.form.is_valid():

            nome = self.form.cleaned_data['nome']
            data_nascimento = self.form.cleaned_data['data_nascimento']

            autor, created = Autor.objects.get_or_create(nome=nome, data_nascimento=data_nascimento)

            autor.save()

            self.assertTrue(Autor.objects.filter(pk=autor.id).exists())


class CreateEditoraViewTestCase(TestCase):

    def setUp(self):
        self.dados = {
            'rua': 'rua',
            'bairro': 'bairro',
            'cidade': 'cidade',
            'estado': 'estado',
            'numero': '1',
            'nome': 'editora'
        }
        self.cliente = Client()
        self.form = EditoraCreateForm(data=self.dados)

    def test_GET(self):

        request = self.client.get(reverse_lazy('livraria:cadastrareditora'), {'form':self.form})

        self.assertEquals(request.status_code, 302)
        self.assertTrue(self.form.is_valid())
        
    def test_POST(self):

        request = self.client.post(reverse_lazy('livraria:cadastrareditora'), {'form':self.form})

        self.assertEquals(request.status_code, 302)
        self.assertTrue(self.form.is_valid())

        if self.form.is_valid():
            rua = self.form.cleaned_data['rua']
            bairro = self.form.cleaned_data['bairro']
            cidade = self.form.cleaned_data['cidade']
            estado = self.form.cleaned_data['estado']
            numero = self.form.cleaned_data['numero']
            nomeEditora = self.form.cleaned_data['nome']

            endereco, created = Endereco.objects.get_or_create(rua=rua, bairro=bairro, numero=numero, cidade=cidade, estado=estado)
            editora, created = Editora.objects.get_or_create(nome=nomeEditora, endereco=endereco)

            editora.save()

            self.assertTrue(Editora.objects.filter(pk=editora.id).exists())
        

class CreateEmprestimoLivroTesteCase(TestCase):

    def setUp(self):
        
        self.user = mommy.make('CustomUsuario', first_name='Primeiro nome', last_name='Ultimo nome')
        self.livro = mommy.make('Livro', estoque=10) 
        self.dados = {
            'quantidade': '1',
            'data_devolucao': '2020-12-20',
            'preco': '20' 
        }

        self.form = EmprestimoLivroCreationForm(data=self.dados)

    def test_POST(self):
        
        if self.form.is_valid():

            quantidade = self.form.cleaned_data['quantidade']
            data_inicial = self.form.cleaned_data['data_inicial']
            data_devolucao = self.form.cleaned_data['data_devolucao']
            preco_total = self.form.cleaned_data['preco']
            diferenca_data = data_devolucao - data_inicial
            
            self.assertEquals(quantidade, 1)
            self.assertLessEqual(diferenca_data.days, 89)
            self.assertLessEqual(quantidade, self.livro.estoque)

            calculo_emprestimo = self.livro.preco * quantidade

            emprestimo, created = EmprestimoLivro.objects.get_or_create(user=self.user,livro=self.livro, data_inicial=data_inicial, data_devolucao=data_devolucao, preco=calculo_emprestimo,ativo=True,quantidade=quantidade)

            self.livro.preco_total = self.livro.preco_total - calculo_emprestimo

            self.livro.save()
            emprestimo.save()

            self.assertTrue(Livro.objects.filter(pk=self.livro.id).exists())
            self.assertTrue(EmprestimoLivro.objects.filter(pk=emprestimo.id).exists())

