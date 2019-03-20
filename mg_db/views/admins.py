from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.generic.base import View

from mg_db.models import Page, Language, PageLanguage, DoesNotExist, CategoryPage
from mg_db.views.page import MyView


@login_required
def test(request):
    pages = Page.objects.all()
    languages = Language.objects.all()
    lange = Language.objects.get(is_default=True)
    lang_all = []
    categories = CategoryPage.objects.all()
    return render(request, 'mg_db/test.html', {'pages': pages, 'languages': languages, 'lang_all': lang_all,
                                               'categories': categories, 'def_lang': lange})


@login_required
def add_page(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    language = request.POST.get('language')
    categor = request.POST.get('category')
    url = request.POST.get('url')
    page = Page(title=title, category=categor, url=url)
    page.save()
    page_language = PageLanguage(page=page, language=language, content=content)
    page_language.save()
    return redirect('test')


@login_required
def add_content(request, page_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        lang = Language.objects.get(id=request.POST.get('lang'))
        page_lang = PageLanguage(content=content, language=lang, page=page_id)
        page_lang.save()
        return redirect('add-content', page_id)
    else:
        page = Page.objects.get(id=page_id)
        language_list = [lang for lang in PageLanguage.objects.filter(page=page)]
        langs = Language.objects.all()
        return render(request, 'mg_db/add_content.html', {'lang_added_list': language_list, 'langs': langs, 'page': page})


@login_required
def delete_content(request, content_id):
    content = PageLanguage.objects.get(id=content_id)
    page = content.page.id
    content.delete()
    return redirect('add-content', page)


@login_required
def language(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        meta_name = request.POST.get('meta_name')
        is_default = True if request.POST.get('is_default') == 'true' else False
        lang = Language(name=name, meta_name=meta_name, is_default=is_default)
        lang.save()
        return redirect('test')
    else:
        lang_all = Language.objects.all()
        return render(request, 'mg_db/language.html', {'lang': 'lang', 'lang_all': lang_all})


@login_required
@require_POST
def default_language(request):
        lang_id = request.POST.get('def_lang')
        language_def = Language.objects.get(id=lang_id)
        Language.objects.all().update(is_default=False)
        language_def.is_default = True
        language_def.save()
        return redirect('test')


@login_required
def category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        cat = CategoryPage(name=name)
        cat.save()
        return redirect('test')
    else:
        return render(request, 'mg_db/language.html')


class AdminMan(View, MyView):

    functions = {'language': language,
                 'test': test,
                 'category': category,
                 'default_language': default_language,
                 'delete_content': delete_content,
                 'add_content': add_content,
                 'add_page': add_page,
                 }

    def dispatch(self, request, *args, **kwargs):
        print(request.resolver_match.url_name)
        return self.functions[request.resolver_match.url_name](request)
        # return super(AdminMan, self).dispatch(request, *args, **kwargs)

    # def get(self, request):
    #
    #     return JsonResponse({'status': 'ok'})
