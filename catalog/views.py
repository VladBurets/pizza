from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import CreateUser, LoginUser, PizzaForm
from catalog.models import Pizza


class CatalogView(TemplateView):
    """
    Страница с каталогом
    """
    template_name = 'catalog/catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Pizza.objects.all()
        # фильтры(берется из параметров GET запроса)
        filters = {i: self.request.GET[i] for i in self.request.GET if i.endswith('__exact')}
        queryset = queryset.filter(**filters)
        # сортировка(берется из параметров GET запроса)(берется из параметров GET запроса)
        if order := self.request.GET.get('order_by'):
            queryset = queryset.order_by(order)
        # поиск(берется из параметров GET запроса)
        if name := self.request.GET.get('q'):
            queryset = queryset.filter(name__icontains=name)
        context['catalog_records'] = queryset
        context['active'] = 'catalog'
        return context


class AuthorizationView(LoginView):
    """
    Страница с формай авторизации
    """
    template_name = 'app/login.html'
    form_class = LoginUser  # класс формы

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'login'
        return context

    def get_success_url(self):
        # срабатывает при успешной авторизации
        # перенаправляет пользователя по url из парраметра запроса 'next' или на страницу католога
        return self.request.GET.get('next', reverse_lazy('catalog'))


class RegisterView(CreateView):
    """
    Страница с формой регистрации
    """
    template_name = 'app/logup.html'
    form_class = CreateUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'login'
        return context

    def form_valid(self, form):
        """
        Если форма валидная
        Сохраняет ползователя в БД и авторизует его
        и перенаправляет на страницу каталога
        """
        user = form.save()
        login(self.request, user)
        return redirect('catalog')


def logout_view(request):
    """выход"""
    logout(request)
    return redirect('catalog')


class AddPizzaView(CreateView):
    """страница добавления пиццы(методы реализованы в классе CreateView)"""
    model = Pizza
    form_class = PizzaForm
    template_name = 'catalog/pizza.html'
    success_url = reverse_lazy('add_pizza')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'add-pizza'
        return context


class PizzaView(UpdateView):
    """Редактирование пиццы(методы реализованы в классе UpdateView)"""
    model = Pizza
    form_class = PizzaForm
    template_name = 'catalog/pizza.html'
    success_url = reverse_lazy('catalog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'add-pizza'
        return context


class DeletePizzaView(DeleteView):
    """очевидно я думаю"""
    model = Pizza
    success_url = reverse_lazy('catalog')
