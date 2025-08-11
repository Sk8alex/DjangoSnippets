from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm
from django.contrib import auth



def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    #ПУстая форма при запросе ГЕТ
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)
    #Получаем данные из формы и на их основе создаём новый снипет, сохраняя в БД

    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets-list") #URL для списка сниппетов
        return render(request, "pages/add_snippet.html", context={"form": form})




def snippets_page(request):
    context = {
        'pagename': 'Все сниппеты',
        'snippets': Snippet.objects.all(),
        'snippets_count': Snippet.objects.count()
        }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id: int):
    context = {'pagename': 'Просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return render(request, 'pages/errors.html', context | {"error": f"Сниппет с id={snippet_id} не найден"})
    else:
        context['snippet'] = snippet
        return render(request, 'pages/snippet_detail.html', context)
    

# def create_snippet(request):
#     if request.method == "POST":
#         form = SnippetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("snippets-list") #URL для списка сниппетов
#         return render(request, "pages/add_snippet.html", context={"form": form})
#     return HttpResponseNotAllowed(["POST"], "You must make POST request to add snippet.")


def snippet_delete(request, snippet_id: int):
    if request.method == "GET" or request.method == "POST":
        snippet = get_object_or_404(Snippet, id=snippet_id)
        snippet.delete()
    return redirect("snippets-list")



def snippet_edit(request, snippet_id: int):
    pass


def login(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       # print("username =", username)
       # print("password =", password)
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           # Return error message
           pass
   return redirect('home')



def logout(request):
    auth.logout(request)
    return redirect(to="home")
