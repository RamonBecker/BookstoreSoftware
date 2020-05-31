from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone



class Produto(models.Model):
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preco', max_digits=8, decimal_places=2)
    estoque = models.IntegerField('Estoque', default=0)
    preco_total = models.DecimalField('Preco Total', max_digits=8, decimal_places=2, default=0)
    def __str__(self):
        return "'{}-{}-{}'".format(self.nome, self.preco, self.estoque)


class Autor(models.Model):
    nome = models.CharField('Nome do autor', max_length=200)
    data_nascimento = models.DateField('Data de nascimento do autor', blank=True)

    def __str__(self):
        return "'{}'-'{}'".format(self.nome,self.data_nascimento)


class Livro(Produto):
    autor = models.ForeignKey('Autor', on_delete=models.CASCADE, related_name='autor')
    edicao = models.IntegerField('Edicao', default=1)
    ano = models.DateField('Ano', blank=True)
    num_paginas = models.IntegerField('Numero de paginas', default=0)
    descricao = models.CharField('Descricao', max_length=300)
    editora = models.ForeignKey('Editora', on_delete=models.CASCADE, related_name='editora')
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='categoria',default='')

    def __str__(self):
        return "'{}'-'{}'-'{} - {}'".format(self.autor, self.edicao, self.ano, self.editora.nome)


class Editora(models.Model):
    nome = models.CharField('Nome', max_length=100)
    endereco = models.ForeignKey('Endereco', on_delete=models.CASCADE, related_name='endereco')

    def __self__(self):
        return "'{} - {}'".format(self.nome, self.endereco)

class Endereco(models.Model):
    rua = models.CharField('Rua', max_length=200)
    bairro = models.CharField('Bairro', max_length=200)
    cidade = models.CharField('Cidade', max_length=200)
    estado = models.CharField('Estado', max_length=200)
    numero = models.IntegerField('Numero', default=0)
    
    def __str__(self):
        return "'{}'-'{}'-'{} - {} - {}'".format(self.rua, self.bairro, self.cidade, self.estado,self.numero)

class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=200)


class EmprestimoLivro(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    livro = models.ForeignKey('Livro',on_delete=models.CASCADE, related_name='livro')
    data_inicial = models.DateTimeField(blank=True)
    data_devolucao = models.DateField(blank=True)
    preco = models.DecimalField('Preco', max_digits=8, decimal_places=2)
    ativo = models.BooleanField(default=False)
    quantidade = models.IntegerField('Quantidade', default=0)

    def __str__(self):
        return "'{}'-{}-{}-{}-{}-{}-{}".format(self.user, self.livro, self.data_inicial, self.data_devolucao, self.preco, self.ativo, self.quantidade)