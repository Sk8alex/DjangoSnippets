from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    context = {
        'pagename': 'Все сниппеты',
        'snippets': Snippet.objects.all(),
        'snippets_count': Snippet.objects.count()
        }
    return render(request, 'pages/view_snippets.html', context)


def snippet_info(request, snippet_id: int):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except Snippet.DoesNotExist:
        raise Http404(f"Сниппет с id={snippet_id} не найден")
    else:
        context = {
            'pagename': 'Сниппет',
            'snippet': snippet,
        }
        return render(request, 'pages/snippet_info.html', context)

