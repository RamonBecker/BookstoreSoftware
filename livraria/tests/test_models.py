from django.test import TestCase
from model_mommy import mommy

class AutorTestCase(TestCase):
    
    def setUp(self):
        self.autor = mommy.make('Autor')
    
    def test_str(self):
        self.assertEquals(str(self.autor), self.autor.nome)


class LivroTestCase(TestCase):

    def setUp(self):
        self.livro = mommy.make('Livro')

    def test_str(self):
        self.assertEquals(str(self.livro), self.livro.nome)


class EditoraTestCase(TestCase):

    def setUp(self):
        self.editora = mommy.make('Editora')

    def test_str(self):
        self.assertEquals(str(self.editora), self.editora.nome)

class EnderecoTestCase(TestCase):

    def setUp(self):
        self.endereco = mommy.make('Endereco')

    def test_str(self):
        self.assertEquals(str(self.endereco.rua), self.endereco.rua)
        self.assertEquals(str(self.endereco.bairro), self.endereco.bairro)
        self.assertEquals(str(self.endereco.estado), self.endereco.estado)
        self.assertEquals(self.endereco.numero, self.endereco.numero)

class CategoriaTestCase(TestCase):

    def setUp(self):
        self.categoria = mommy.make('Categoria')

    def test_str(self):
        self.assertEquals(str(self.categoria), self.categoria.nome)