from django.urls import path
from mg_db.views.admins import test, add_page, language, category, add_content, delete_content, AdminMan
from mg_db.views.auth import login_test, logout_test


urlpatterns = [
    path('', test, name='test'),
    path('logout/', logout_test, name='logout'),
    path('add_content/<str:page_id>', add_content, name='add-content'),
    path('delete_content/<str:content_id>', delete_content, name='delete-lang-content'),
    path('login/', login_test, name='login'),
    path('language/', AdminMan.as_view(), name='language'),
    path('category/', category, name='category'),
    path('add_page/', add_page, name='add-page'),
]