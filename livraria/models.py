from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


from django.contrib.auth.models import AbstractUser, BaseUserManager 


class UsuarioManager(BaseUserManager):
    use_in_migrations = True  # Estamos avisando ao Django, que esse será o nosso modelo que usaremos em nosso banco

    # de dados

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Fazendo método para criar usuário comum
    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    # Fazendo método para criar super usuário
    def create_superuser(self, email, password, **extrafields):
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_staff', True)

        # Verificando se é super usuario
        if extrafields.get('is_superuser') is not True:
            raise ValueError('Super usuário precisa ter is_superuser como True')
        # Se for false o usuário não terá acesso ao painel administrativo do Django
        if extrafields.get('is_staff') is not True:
            raise ValueError('Super usuário precisa ter is_staff como True')

        return self._create_user(email, password, **extrafields)


class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    fone = models.CharField('Telefone', max_length=15)
    is_staff = models.BooleanField('Membro da equipe', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fone']


    def __str__(self):
        return self.email

    objects = UsuarioManager()




class Produto(models.Model):
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preco', max_digits=8, decimal_places=2)
    estoque = models.IntegerField('Estoque', default=0)
    preco_total = models.DecimalField('Preco Total', max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return "'{}-{}-{}'".format(self.nome, self.preco, self.estoque)


class Autor(models.Model):
    nome = models.CharField('Nome do autor', max_length=200)
    data_nascimento = models.DateField('Data de nascimento do autor')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return "'{}'-'{}'".format(self.nome,self.data_nascimento)


class Livro(Produto):

    autor = models.OneToOneField('Autor', on_delete=models.CASCADE, related_name='autor')
    editora = models.OneToOneField('Editora', on_delete=models.CASCADE, related_name='editora')
    edicao = models.IntegerField('Edicao', default=1)
    ano = models.DateField('Ano')
    num_paginas = models.IntegerField('Numero de paginas', default=0)
    descricao = models.CharField('Descricao', max_length=300)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='categoria')

    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

    def __str__(self):
        return "'{}'-'{}'-'{} - {}'".format(self.autor, self.edicao, self.ano, self.editora.nome)


class Editora(models.Model):
    nome = models.CharField('Nome', max_length=100)
    endereco = models.OneToOneField('Endereco', on_delete=models.CASCADE, related_name='endereco')

    class Meta:
        verbose_name = 'Editora'
        verbose_name_plural = 'Editoras'

    def __self__(self):
        return "'{} - {}'".format(self.nome, self.endereco)


class Endereco(models.Model):
    rua = models.CharField('Rua', max_length=200)
    bairro = models.CharField('Bairro', max_length=200)
    cidade = models.CharField('Cidade', max_length=200)
    estado = models.CharField('Estado', max_length=200)
    numero = models.IntegerField('Numero', default=0)
    
    class Meta:
        verbose_name = 'Endereco'
        verbose_name_plural = 'Enderecos'

    def __str__(self):
        return "'{}'-'{}'-'{} - {} - {}'".format(self.rua, self.bairro, self.cidade, self.estado,self.numero)


class Categoria(models.Model):


    CATEGORIA_CHOICES = (
        ('Filosofia', 'Filosofia'),
        ('Religiao','Religiao'),
        ('Ciencia','Ciencia'),
        ('Romance','Romance'),
        ('Historia','Historia'),
    )

    nome = models.CharField('Nome', max_length=200, choices=CATEGORIA_CHOICES)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return "'{}'".format(self.nome)



class EmprestimoLivro(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    livro = models.ForeignKey('Livro',on_delete=models.CASCADE, related_name='livro')
    data_inicial = models.DateTimeField('Data inicial', auto_now_add=True)
    data_devolucao = models.DateField('Data de devolução')
    preco = models.DecimalField('Preco', max_digits=8, decimal_places=2)
    ativo = models.BooleanField(default=False)
    quantidade = models.IntegerField('Quantidade', default=0)


    class Meta:
        verbose_name = 'Emprestimo'
        verbose_name_plural = 'Emprestimos'

    def __str__(self):
        return "'{}'-{}-{}-{}-{}-{}-{}".format(self.user, self.livro, self.data_inicial, self.data_devolucao, self.preco, self.ativo, self.quantidade)

