from django.contrib.auth.decorators import login_required
from django.urls import path

from mg_db.views.page import TemplatePage

urlpatterns = [
    path('', login_required(TemplatePage.as_view()), name='page-lang-default'),  # home
    path('<str:url_2>/', login_required(TemplatePage.as_view()), name='page'),
]