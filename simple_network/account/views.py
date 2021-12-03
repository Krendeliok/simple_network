from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, request

from .utils import *
from .forms import AddPostForm, RegisterUserForm, LoginUserForm, SearchForm, SettingsForm
from .models import User, Post


@login_required
def profile_view(request, **kwargs):
    if request.method == "GET" and request.user.is_authenticated:
        user_id = kwargs["id"]
        authenticated_user_id = request.user.id
        edit_permission = False
        if user_id == authenticated_user_id:
            edit_permission = True
        user = User.objects.get(pk=user_id)
        user_posts = Post.objects.all().filter(author_id=user_id).order_by('publish_date')
        return render(
            request, 
            "profile.html", 
            {
                "title": "Профиль",
                "user": user,
                "posts": user_posts,
                "edit_permission": edit_permission
            }
        )
    return HttpResponseNotFound

@login_required
def settings_view(request):
    initial_values = {
        'nickname': request.user.nickname,
        'email': request.user.email,
    }
    if request.method == "GET":
        form = SettingsForm(initial=initial_values)  
    elif request.method == "POST":
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        form = SettingsForm(request.POST, request.FILES, initial=initial_values)
        if form.is_valid():
            data = form.cleaned_data
            errors = False
            if any([data.get('password', None), data.get('repeat_password', None)]):
                if data.get('password') != data.get('repeat_password'):
                    errors = True
                    form.errors["password"] = "Пароли не совпадают"
                else:
                    user.set_password(data.get('password'))
            if User.get_by_nickname(user_id, data.get("nickname")):
                errors = True
                form.errors["nickname"] = "Пользователь с таким именем уже существует"
            if User.get_by_email(user_id, data.get("email")):
                errors = True
                form.errors["email"] = "Пользователь с такой почтой уже существует"
            if not errors:
                if user.nickname != data.get("nickname"):
                    user.nickname = data.get("nickname")
                if user.email != data.get("email"):
                    user.email = data.get("email")
                if request.FILES["photo"]:
                    user.photo = request.FILES["photo"]
                user.save()

    return render(
            request,
            "settings.html",
            {
                "title": "Настройки",
                "form": form
            }
        )

@login_required
def add_post_view(request):
    if request.method == "GET":
        form = AddPostForm()
    elif request.method == "POST":
        user_id = request.user.id
        form = AddPostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.author_id = user_id
            post.post_text = form.cleaned_data.get("post_text")
            post.save()
            return redirect(reverse('profile', kwargs={'id': user_id}))
    return render(
        request,
        'add_post.html',
        {
            "title": "Добавить пост",
            "form": form
        }
    )

@login_required
def delete_post_view(request, **kwargs):
    user_id = request.user.id
    post_to_delete = Post.objects.get(pk=kwargs["post_id"])
    if user_id == post_to_delete.author_id:
        post_to_delete.delete()
    return redirect(reverse('profile', kwargs={'id': user_id}))

@login_required
def search_view(request):
    if request.method == "GET":
        form = SearchForm()
        users = User.objects.all()
    elif request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            users = User.objects.filter(nickname=form.cleaned_data["search_field"])
    return render(
            request,
            "search.html",
            {
                "title": "Поиск",
                "form": form,
                "users": users,
            }
        )

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('login')) 

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        return context
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('profile', kwargs={'id': request.user.id}))
        else: 
            return super().get(self, request)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        return context

    def get_success_url(self):
        return reverse('profile', kwargs={'id': self.request.user.id})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('profile', kwargs={'id': request.user.id}))
        else: 
            return super().get(self, request)
