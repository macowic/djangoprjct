from unicodedata import name
from django.urls import (
    path, re_path
)
from django.conf import settings
from django.conf.urls.static import static
from . import views
from firstapp.views import(
    IndexView,
    LoginView,
    RegisterView,
    LogoutView,
    ShowView,
    AdminView,
    DeleteView,
    HomeworkCreateView,
    HomeworkDetailView,
    HomeworkDeleteView,
    HomeworkFileCheckedView,
    HomeworkFileView
)


urlpatterns = [
    path(
        '',
        IndexView.as_view(),
        name = 'page_main'
    ),
    path(
        'admin/',
        AdminView.as_view(),
        name = 'page_admin'
    ),
    path(
        'show/<int:homework_id>/',
        ShowView.as_view(),
        name='page_show',
    ),
    path(
        'delete/<int:user_id>/',
        DeleteView.as_view(),
        name = 'page_delete'
    ),
    path(
        'register/',
        RegisterView.as_view(),
        name = 'page_register'
    ),
    path(
        'login/',
        views.LoginView.as_view(),
        name = 'page_login'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name = 'page_logout'
    ),
    path(
        'create_hw/',
        HomeworkCreateView.as_view(),
        name = 'page_create'
    ),
    path(
        'detail_hw/', 
        HomeworkDetailView.as_view(),
        name = 'page_homework_detail'  
    ),
    path(
        'delete_hw/',
        HomeworkDeleteView.as_view(),
        name='page_homework_delete'
    ),
    path(
        'file_create/',
        HomeworkFileView.as_view(),
        name='page_homework_file_create'    
    ),
    path(
        'file_check/',
        HomeworkFileCheckedView.as_view(),
        name='page_homework_file_checked'
    ),
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

