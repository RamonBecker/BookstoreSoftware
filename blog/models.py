from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model): # Utilizando Herança com Python Post é um Model
    # Definindo a chave estrangeira 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()


    create_date = models.DateField(auto_now=True)

    #definindo data e hora e o campo pode ser nulo
    published_date = models.DateField(blank=True, null=True)

    def publish(self):
        #Pega a data e hora atual e altera a data de publicação para realizar o salvamento de dados no banco de dados
        self.published_date = timezone.now()
        self.save()

    def __str__(self): #Retorna a string do objeto em memória
        return '{} ({})'.format(self.title, self.author)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

