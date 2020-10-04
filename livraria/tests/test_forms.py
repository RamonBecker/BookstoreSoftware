from django.test import TestCase
from model_mommy import mommy
from livraria.forms import CustomUsuarioCreationForm, AutorCreationForm


class CustomUsuarioCreationFormTestCase(TestCase):

    def setUp(self):
        self.user = mommy.make('CustomUsuario', first_name='Primeiro nome', last_name='Ultimo nome')
        self.dados = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'fone': self.user.fone,
            'email': self.user.email,
            'password1': self.user.password,
            'password2': self.user.password,
        }
        self.form = CustomUsuarioCreationForm(data=self.dados)
       
    def test_save(self):

        res1 = None
        res2 = None

        form1 = CustomUsuarioCreationForm(data=self.dados)

        if form1.is_valid():
            res1 = form1.save()

        form2 = self.form

        if form2.is_valid():
            res2 = form2.save()
        self.assertEquals(res1, res2)
    
