from django import forms
from livraria.models import Livro, Editora, Endereco, Autor, EmprestimoLivro
from django.utils import timezone
from datetime import date

CATEGORIAS_LIVROS = [
    ('','Selecione'),
    ('Filosofia', 'Filosofia'),
    ('Religiao','Religiao'),
    ('Ciencia','Ciencia'),
    ('Romance','Romance'),
]

class DateInput(forms.DateInput):
    input_type = 'date'

class CheckboxInput(forms.CheckboxInput):
    input_type = 'checkbox'

class LivroForm(forms.ModelForm):
    ano = forms.DateField(widget=DateInput)

    list_editoras = Editora.objects.all().values()

    editora = forms.ChoiceField(choices=[('0','Selecione')]+ [(editora.id, editora.nome) for editora in  Editora.objects.all()])
    descricao = forms.CharField(widget=forms.Textarea())
    categorias = forms.ChoiceField(choices=CATEGORIAS_LIVROS)

   # categoria_nao_encontrada = forms.BooleanField(required=False, label='Não encontrei minha categoria')
    class Meta:
        model = Livro
        fields = ('nome', 'preco','estoque', 'edicao','num_paginas')

class EditoraForm(forms.ModelForm):
    class Meta:
        model = Editora
        fields = ('nome',)

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ('rua','bairro','cidade','estado','numero')

class AutorForm(forms.Form):
   
    nomeAutor = forms.CharField(max_length=100,label='Nome do autor')
    ano = forms.DateField(widget=DateInput,label='Ano de nascimento do autor')

class EmprestimoForm(forms.Form):
    data_inicial = forms.DateField(label='Data de início',disabled=True,initial=timezone.now)
    data_devolucao = forms.DateField(label='Data de devolução',widget=DateInput)
    quantidade = forms.IntegerField(label='Quantidade a ser emprestada', initial=0)
    preco = forms.DecimalField(label='Preco a pagar pelo emprestimo',decimal_places=2,disabled=True, initial=0)
  
class Livro_Emprestimo_Form(forms.ModelForm):
    nome = forms.CharField(required=True,max_length=100)
    class Meta:
        model = Livro
        fields = ('nome',)


