from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django import forms
from django.utils import timezone
from datetime import datetime, date
from django.conf import settings


from .models import CustomUsuario, Livro, Editora, Categoria, Autor, EmprestimoLivro
from mysite.settings import DATE_INPUT_FORMATS, TIME_INPUT_FORMATS

class DateInput(forms.DateInput):
    input_type = 'date'
    


CATEGORIA_CHOICES = (
    ('Filosofia', 'Filosofia'),
    ('Religiao','Religiao'),
    ('Ciencia','Ciencia'),
    ('Romance','Romance'),
    ('Historia','Historia'),
    ('Terror', 'Terror'),
    ('Suspense', 'Suspense'),
    )


class CustomUsuarioCreationForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone', 'email')


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data['email']
        

        if commit:
            user.save()

        return user


class CustomUsuarioChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=("Senha"),
        help_text=("Para atualizar a senha, você precisa clicar no botão de atualizar senha abaixo"))
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone', 'email')


class LivroCreationForm(forms.ModelForm):

    categoria = forms.ChoiceField(choices=CATEGORIA_CHOICES, label='Categoria')
    ano = forms.DateField(widget=DateInput, label='Ano')
    descricao = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Livro
        fields = ('nome', 'preco', 'estoque', 'edicao', 'num_paginas', 'autor', 'editora')


class EditoraCreateForm(forms.ModelForm):
    rua = forms.CharField(max_length=100,label='Rua')
    bairro = forms.CharField(max_length=100,label='Bairro')
    numero = forms.IntegerField(initial = 0,label='Número')
    cidade = forms.CharField(max_length=100,label='Cidade')
    estado = forms.CharField(max_length=100,label='Estado')

    class Meta:
        model = Editora
        fields = ('nome',)


class AutorCreationForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DateInput, label='Data de nascimento')

    class Meta:
        model = Autor
        fields = ('nome',)


class EmprestimoLivroCreationForm(forms.ModelForm):
    data_inicial = forms.DateField(label='Data de início',disabled=True,initial=date.today)
    data_devolucao = forms.DateField(widget=DateInput, label='Digite a data de devolução')
    preco = forms.DecimalField(label='Preco a pagar pelo emprestimo',decimal_places=2,disabled=True, initial=0)
    
    
    class Meta:
        model = EmprestimoLivro
        fields = ('quantidade', )




