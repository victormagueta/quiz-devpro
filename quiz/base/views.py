from django.shortcuts import render, redirect

# Create your views here.
from quiz.base.models import Pergunta, Aluno
from quiz.base.forms import AlunoForm


def home(requisicao):
    if requisicao.method == 'POST':
        #Usuário já existe
        email = requisicao.POST['email']

        try:
            aluno = Aluno.objects.get(email=email)
        except Aluno.DoesNotExist:
            #usuário não existe
            formulario = AlunoForm(requisicao.POST)
            if formulario.is_valid():
                aluno = formulario.save()
                requisicao.session['aluno_id'] = aluno.id
                return redirect('/perguntas/1')
            else:
                contexto = {'formulario' : formulario}
                return render(requisicao, 'base/home.html', contexto)
        else:
            requisicao.session['aluno_id'] = aluno.id
            return redirect('/perguntas/1')

    return render(requisicao, 'base/home.html')

def classificacao(requisicao):
    return render(requisicao, 'base/classificacao.html')

def perguntas(requisicao, indice):
    try:
        aluno_id = requisicao.session['aluno_id']
    except KeyError:
        return redirect('/')
    else:   
        pergunta = Pergunta.objects.filter(disponivel = True).order_by('id')[indice - 1]
        contexto = {'indice_da_questao' : indice, 'pergunta' : pergunta}
        if requisicao.method == 'POST':
            resposta_indice = int(requisicao.POST['resposta_indice'])
            if resposta_indice == pergunta.alternativa_correta:
                #Armazenar dados da resposta
                return redirect(f'/perguntas/{indice + 1}')
            contexto['resposta_indice'] = resposta_indice
        return render(requisicao, 'base/game.html', context=contexto)
