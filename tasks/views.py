from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
#Para criar mensagens de confirmação ao deletar/atualizar
from django.contrib import messages
#paginação
from django.core.paginator import Paginator

def taskList(request):
    #Lista todos os registros do banco e os ordena por data de criação
    tasks_list = Task.objects.all().order_by('-created_at')
    #Reserva o espaço de 3 itens por página
    paginador = Paginator(tasks_list, 3)
    #Número a página
    page = request.GET.get('page')
    #Mostra os itens de cada página
    tasks = paginador.get_page(page)
    return render(request, 'tasks/lista.html', {'tasks':tasks})

def taskView(request, id):
    #Visualiza uma tarefa em particular selecionada pelo id
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task' : task})

def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.save()
            messages.info(request, "Tarefa adicionada!")
            #redireciona para a página lista.html
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})

def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    #deixa o formulário já preenchido para a edição
    form = TaskForm(instance=task)

    if (request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)
        if (form.is_valid()):
            task.save()
            messages.info(request, "Edições realizadas com sucesso!")
            return redirect('/')
        else:
            return render(request, 'tasks/edittask.html', {'form': form, 'task': task})                
    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task': task})

def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    messages.info(request, "Tarefa deletada com sucesso!")
    return redirect('/')

def helloWorld(request):
    return HttpResponse('Hello world!')

def yourName(request, name):
    context = {
        'name' : name
    }
    return render(request, 'tasks/yourName.html', context)
