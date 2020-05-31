# Generated by Django 3.0.6 on 2020-05-23 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome do autor')),
                ('data_nascimento', models.DateField(blank=True, verbose_name='Data de nascimento do autor')),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rua', models.CharField(max_length=200, verbose_name='Rua')),
                ('bairro', models.CharField(max_length=200, verbose_name='Bairro')),
                ('cidade', models.CharField(max_length=200, verbose_name='Cidade')),
                ('estado', models.CharField(max_length=200, verbose_name='Estado')),
                ('numero', models.IntegerField(default=0, verbose_name='Numero')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preco')),
                ('estoque', models.IntegerField(default=0, verbose_name='Estoque')),
            ],
        ),
        migrations.CreateModel(
            name='Editora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='endereco', to='livraria.Endereco')),
            ],
        ),

        
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('produto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='livraria.Produto')),
                ('edicao', models.IntegerField(default=1, verbose_name='Edicao')),
                ('ano', models.DateField(blank=True, verbose_name='Ano')),
                ('genero', models.CharField(max_length=100, verbose_name='Genero')),
                ('num_paginas', models.IntegerField(default=0, verbose_name='Numero de paginas')),
                ('descricao', models.CharField(max_length=300, verbose_name='Descricao')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autor', to='livraria.Autor')),
                ('editora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editora', to='livraria.Editora')),
            ],
            bases=('livraria.produto',),
        ),
    ]