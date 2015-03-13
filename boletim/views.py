from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from models import Disciplina, Lembrete
from forms import FormDisciplina, FormAnotacao

@login_required
def index(request):
    lista_disciplinas = Disciplina.objects.filter(usuario=request.user)

    return render(request, "disciplinas.html",
                  {"lista_disciplinas": lista_disciplinas},context_instance=RequestContext(request))

@login_required
def lembretes(request):
    lista_lembretes = Lembrete.objects.filter(usuario=request.user)

    return render(request, "lembretes.html",
                  {"lista_lembretes": lista_lembretes},context_instance=RequestContext(request))

@login_required
def adiciona(request):
    if request.method == "POST":
        form = FormDisciplina(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.usuario = request.user
            item.save()
            return render(request, "aviso_salvo.html", {})
    else:
        form = FormDisciplina()
    return render(request, "adiciona.html", {"form": form},
                  context_instance=RequestContext(request))

@login_required
def lembrete(request):
    if request.method == "POST":
        form = FormAnotacao(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.usuario = request.user
            item.save()
            return render(request, "aviso_lembrete_salvo.html", {})
    else:
        form = FormAnotacao()
    return render(request, "addlembrete.html", {"form": form},
                  context_instance=RequestContext(request))

@login_required
def item(request, id_disciplina):
    disciplina = get_object_or_404(Disciplina, pk=id_disciplina, usuario=request.user)
    if request.method == "POST":
        form = FormDisciplina(request.POST, request.FILES, instance=disciplina)
        if (form.is_valid()):
            item = form.save(commit=False)
            item.usuario = request.user
            item.save()
            return render(request, "aviso_salvo.html", {})
    else:
        media = (disciplina.n1+disciplina.n2+disciplina.n3)/3
        form = FormDisciplina(instance=disciplina)
    return render(request, "item.html",{'form': form, 'media': media}, context_instance=RequestContext(request))

@login_required
def item_lembrete(request, id_lembrete):
    lembrete = get_object_or_404(Lembrete, pk=id_lembrete, usuario=request.user)
    if request.method == "POST":
        form = FormAnotacao(request.POST, request.FILES, instance=lembrete)
        if (form.is_valid()):
            item = form.save(commit=False)
            item.usuario = request.user
            item.save()
            return render(request, "aviso_lembrete_salvo.html", {})
    else:
        form = FormAnotacao(instance=lembrete)
    return render(request, "item_lembrete.html",{'form': form}, context_instance=RequestContext(request))

@login_required
def remove(request, id_disciplina):
    disciplina = get_object_or_404(Disciplina, pk=id_disciplina, usuario=request.user)
    if(request.method == "POST"):
        disciplina.delete()
        return render(request, "aviso_removido.html", {})
    return render(request, "remover.html",{'disciplina': disciplina}, context_instance=RequestContext(request))

@login_required
def remove_lembrete(request, id_lembrete):
    lembrete = get_object_or_404(Lembrete, pk=id_lembrete, usuario=request.user)
    if(request.method == "POST"):
        lembrete.delete()
        return render(request, "aviso_lembrete_removido.html", {})
    return render(request, "remover_lembrete.html",{'lembrete': lembrete}, context_instance=RequestContext(request))

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/boletim/index.html')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Sua conta esta desativada!")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('boletim/login.html', {}, context)