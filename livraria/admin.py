from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
'''
from .forms import CustomUsuarioCreationForm, CustomUsuarioChangeForm
from .models import CustomUsuario


@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreationForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario
    list_display = ('first_name', 'last_name', 'email', 'fone', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'fone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )


from .models import Editora, Endereco, Autor, Livro, Categoria, EmprestimoLivro

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome','data_nascimento')

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('rua','bairro','cidade','numero','estado')

@admin.register(Livro)
class Livro(admin.ModelAdmin):
    list_display = ('nome','preco','estoque','autor','editora','descricao','num_paginas','ano','edicao', 'categoria')


@admin.register(Editora)
class Editora(admin.ModelAdmin):
    list_display = ('nome','endereco')


@admin.register(Categoria)
class Categoria(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(EmprestimoLivro)
class Emprestimo(admin.ModelAdmin):
    list_display = ('user', 'livro','data_inicial','data_devolucao','preco','ativo','quantidade')'''