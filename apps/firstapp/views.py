from re import template
from turtle import home
from typing import Optional
from urllib import request

from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.template import loader
from django.contrib.auth import (
    authenticate as dj_authenticate,
    login as dj_login,
    logout as dj_logout,
)

from abstracts.mixins import HttpResponseMixin
from abstracts.handlers import ViewHandler
from auths.forms import CustomUserForm
from firstapp.forms import HomeworkForm
from auths.models import CustomUser
from .models import (
    Account,
    Homework,
    File,
    Student,
)

class IndexView(ViewHandler,View):

    queryset: QuerySet = \
        Homework.objects.get_not_deleted()
    
    def get(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs : dict
    ) -> HttpResponse:
        """Get request handler"""

        response: Optional[HttpResponse] = \
            self.get_validated_response(
                request
            )
        if response:
            return response

        if not request.user.is_authenticated:
            return render(
                request,
                'firstapp/index.html'
            )
        homeworks : QuerySet = self.queryset.filter(
            user = request.user,
        )
        if not homeworks:
            homeworks = self.queryset

        context: dict = {
            'ctx_title' : 'Главная страница',
            'ctx_homeworks' : homeworks,
        }

        template_name: str = 'firstapp/index.html'

        return self.get_http_response(
            request, 
            template_name,
            context
        )

class HomeworkCreateView(ViewHandler, View):

    form: HomeworkForm = HomeworkForm
    template_name: str = 'firstapp/homework_create.html'

    def get(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """GET request handler."""

        response: Optional[HttpResponse] = \
            self.get_validated_response(
                request
            )
        if response:
            return response

        context: dict = {
            'form': self.form(),
        }
        return self.get_http_response(
            request,
            self.template_name,
            context
        )

    def post(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """POST request handler."""

        _form: HomeworkForm = self.form(
            request.POST or None,
            request.FILES or None
        )
        if not _form.is_valid():
            context: dict = {
                'ctx_form': _form,
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )
        homework: Homework = _form.save(
            commit=False
        )
        homework.user = request.user
        homework.logo = request.FILES['logo']

        file_type: str = homework.logo.url.split('.')[-1].lower()

        if file_type not in Homework.IMAGE_TYPES:

            context: dict = {
                'ctx_form': _form,
                'ctx_homework': homework,
                'error_message': 'PNG, JPG, JPEG',
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )
        homework.save()

        context: dict = {
            'homework': homework
        }
        return self.get_http_response(
            request,
            'firstapp/homework_detail.html',
            context
        )
      
        
class HomeworkDetailView(ViewHandler, View):
    pass


class HomeworkFileCheckedView(ViewHandler, View):
    
    pass

class HomeworkFileView(ViewHandler, View):
    
    pass

class HomeworkDeleteView(ViewHandler, View):
    
    pass
            
class ShowView(ViewHandler,View):

    queryset: QuerySet = Homework.objects.get_not_deleted()

    template_name : str = 'firstapp/show.html'

    def get(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ):

        homework_id: int = kwargs.get('homework_id', 0)
        print("Homework id:", homework_id)
        print("User id:", request.user.id)
        # user: CustomUser = CustomUser.objects.get(
        #     id = user_id
        # )

        homework: Optional[Homework] = None
        try:
            homework = self.queryset.get(
                id=homework_id
                )
        except Homework.DoesNotExist as e:
            return self.get_http_response(
                request,
                'firstapp/index.html'
            )
        else:
            context: dict = {
                'ctx_title' : 'Домашние задания',
                'ctx_homework' : homework, 
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )


class AdminView(ViewHandler, View):

    def get(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:

        template_name : str = 'firstapp/admin.html'

        users: QuerySet = CustomUser.objects.filter(
            is_active = True
        )

        context: dict = {
            "users": CustomUser.objects.all()
        }
        return self.get_http_response(
            request,
            template_name,
            context
        )


class DeleteView(ViewHandler,View):

    def get(self,
        request: WSGIRequest,
        user_id: int,
        *args: tuple,
        **kwargs: dict,
        ) -> HttpResponse:

        user = CustomUser.objects.get(id=user_id)
        user.is_active = False
        ctx_users: QuerySet = CustomUser.objects.filter(
            is_active=True
        )
        print(ctx_users)

        context: dict = {
            'ctx_title': 'Главная страница',
            'ctx_users': ctx_users,
            }
            
        template_name: str = 'firstapp/admin.html'
        
        return self.get_http_response(
            request,
            template_name,
            context
        )    
        

class RegisterView(ViewHandler,View):

    def get(
        self,
        request : HttpResponse,
        *args: tuple,
        **kwargs : dict):
        form: CustomUserForm = CustomUserForm()
        return render(
            request,
            'firstapp/register.html',
            context={"form": form}
        )

    def post(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict):
        form: CustomUserForm = CustomUserForm(
            request.POST
        )
        if form.is_valid():
            user: CustomUser = form.save(
                commit=False
            )
            email: str = form.cleaned_data['email']
            password: str = form.cleaned_data['password']
            user.email = email
            user.set_password(password)
            user.save()

            user: CustomUser = dj_authenticate(
                email=email,
                password=password
            )
            if user and user.is_active:

                dj_login(request, user)

                homeworks: QuerySet = Homework.objects.filter(
                    user=request.user
                )
                return render(
                    request,
                    'firstapp/index.html',
                    {'homeworks': homeworks}
                )
        context: dict = {
        'form': form
        }

        template_name: str = 'firstapp/index.html'

        return self.get_http_response(
            request,
            template_name,
            context
        )


class LoginView(ViewHandler,View):

    def get(
        self,
        request : HttpResponse,
        *args: tuple,
        **kwargs : dict):
            return render(
                request,
                'firstapp/login.html'
            )

    def post(
        self,
        request : WSGIRequest,
        *args: tuple,
        **kwargs : dict
    ):
        template_name = loader.get_template(
            'firstapp/login.html'
        )

        email: str = request.POST['email']
        password: str = request.POST['password']

        user: CustomUser = dj_authenticate(
            email=email,
            password=password
        )

        if not user:
            return render(
                request,
                'firstapp/login.html',
                {'error_message': 'Неверные данные'}
            )
        if not user.is_active:
            return render(
                request,
                'firstapp/login.html',
                {'error_message': 'Ваш аккаунт был удален'}
            )
        dj_login(request, user)

        homeworks: QuerySet = Homework.objects.filter(
        user=request.user
        )
        context: dict = {
            'ctx_homeworks': homeworks
        }
        template_name: str = 'firstapp/index.html'
        
        return self.get_http_response(
            request,
            template_name,
            context
            
        )


class LogoutView(ViewHandler,View):
    def get(
        self,
        request: HttpResponse,
        *args: tuple,
        **kwargs : dict
    ):
        return render(
                request,
                'firstapp/login.html'
            )
    
    def post(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ):
        template_name : str = 'firstapp/login.html'

        dj_logout(request)

        form: CustomUserForm = CustomUserForm(
            request.POST
        )
        context: dict = {
            'form': form,
        }

        return self.get_http_response(
            request,
            template_name,
            context
        )

