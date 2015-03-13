from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class Disciplina(models.Model):
    nome = models.CharField(max_length=40)
    professor = models.CharField(max_length=40)
    n1 = models.DecimalField(max_digits=4, decimal_places=2)
    n2 = models.DecimalField(max_digits=4, decimal_places=2)
    n3 = models.DecimalField(max_digits=4, decimal_places=2)
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.nome

class Lembrete(models.Model):
    titulo = models.CharField(max_length=30)
    disciplina = models.CharField(max_length=30)
    assunto = models.CharField(max_length=150)
    data = models.DateTimeField(auto_now_add=True, blank=True)
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.titulo