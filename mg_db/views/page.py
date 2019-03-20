from django.contrib.auth.models import User
from django.views import generic
from rest_framework import status
from rest_framework.response import Response

from mg_db.models import Language, Page, PageLanguage

from rest_framework.views import APIView

from mg_db.serializers.user import UserSerializer


class MyView(object):

    def list_language_page_info(self, my_page, meta_name):
        lang_all = []
        for page_lang in PageLanguage.objects.filter(page=my_page):
            page_lang.language.url = page_lang.page.url if my_page.is_home is False else '/'
            page_lang.language.meta_name = page_lang.language.meta_name if meta_name != page_lang.language.meta_name else ' '
            lang_all.append(page_lang.language)
        return lang_all

    def check_content(self, lang_id, page):
        content = None
        if PageLanguage.objects.filter(language=lang_id, page=page).count() != 0:
            content = PageLanguage.objects.get(language=lang_id, page=page).content
        return content

    def check_is_default_language(self, leng):
        language_obj = Language.objects.get(meta_name=leng) if bool(leng) else Language.objects.get(is_default=True)
        language_obj.meta_name = leng if bool(leng) else ' '
        return language_obj


class TemplatePage(generic.TemplateView, MyView):

    template_name = 'mg_db/page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TemplatePage, self).get_context_data(**kwargs)
        if kwargs.get('url') in [lang.meta_name for lang in Language.objects.all()]:
            kwargs['lng'] = kwargs['url']
            kwargs.pop('url')
        if kwargs.get('url_2') is not None:
            kwargs['url'] = kwargs['url_2']
        url, lng = kwargs.get('url'), kwargs.get('lng')
        context['pages'] = Page.objects.all()
        context['page'] = Page.objects.get(url=url) if bool(url) else Page.objects.get(is_home=True)
        context['base_default_lang'] = Language.objects.get(is_default=True).meta_name
        context['language_obj'] = self.check_is_default_language(lng)
        context['current_language_page_info'] = self.list_language_page_info(context['page'], context['base_default_lang'])
        context['content'] = self.check_content(context['language_obj'].id, context['page'])
        return context


class UserList(APIView):

    def get(self, request, format=None):
        snippets = User.objects.get(id=request.user.id)
        serializer = UserSerializer(snippets, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
