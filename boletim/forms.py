from django import forms
from models import Disciplina, Lembrete

class FormDisciplina(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ('nome', 'professor', 'n1', 'n2', 'n3')

class FormAnotacao(forms.ModelForm):
    class Meta:
        model = Lembrete
        fields = ('titulo', 'disciplina', 'assunto')