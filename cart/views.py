"""
Сообсственно представления(обработчики)
get - обрабатывает GET запрос
post - обрабатывает POST запрос
get_context_data - собирает контекст для шаблонизатор(то, что будет доступно в шаблоне/html)

если методы не реадизованы, значит используется реализация по умолчанию в родительском классе
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, DeleteView

from catalog.models import Pizza
from cart.models import Cart


class CartView(LoginRequiredMixin, TemplateView):
    """
    Представление страницы корзины
    """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_records'] = Cart.objects.filter(user=self.request.user)
        context['active'] = 'cart'
        return context


class DeleteCartRecord(LoginRequiredMixin, DeleteView):
    """
    Удаляет запись из корзины
    """
    model = Cart
    success_url = reverse_lazy('cart')


class CreateCartOrder(LoginRequiredMixin, View):
    """
    Создает запись в таблице с "добавленным" в корзине пользователя
    """

    def post(self, request, pk, **kwargs):
        c_user = self.request.user  # текущий пользователь
        c_pizza = Pizza.objects.get(pk=pk)  # пицца, которую он выбрал
        # проверка на этого пользователя и эту пиццу(если она у него уже добавлена )
        if not Cart.objects.filter(user=c_user).filter(pizza=c_pizza):
            new_order = Cart(user=c_user, pizza=c_pizza)  # добавление и сохранение
            new_order.save()
        return redirect('catalog') # тут пишется имя, которое указано в файле urls.py


@require_POST
def crement(request, pk: int, ct=None):
    """
    изменяет количество пиццы в корзине
    ct передается в urls.py в kwargs={ ...
    pk берется из строки запроса
    """
    cart_record = Cart.objects.get(pk=pk)
    match ct:
        case '+':
            cart_record.count += 1
        case '-':
            cart_record.count -= 1 if cart_record.count > 1 else 0
        case _:
            print(f'\nct is {ct}(must be a +/- )\n')
            return redirect('catalog')
    cart_record.save()
    return redirect('cart')


class ClearCart(LoginRequiredMixin, View):
    """
    Очистка корзины
    """
    def post(self, request):
        Cart.objects.filter(user=self.request.user).delete()  # удаляет все записи для этого пользователя
        return redirect('cart')


class MakeOrderView(TemplateView):
    """
    Кнопка "оформить заказ" ссылает сюда
    """
    template_name = 'cart/confirm-order.html'

    def get_context_data(self, **kwargs):
        """
        Считает скока денек надо
        """
        context = super().get_context_data(**kwargs)
        context['active'] = 'cart'
        orders = Cart.objects.filter(user=self.request.user)
        price = 0
        for o in orders:
            price += o.pizza.price * o.count
        context['price'] = price
        return context

    def post(self, request, **kwargs):
        # тут была бы логика оформления заказа
        # можно чистить корзину или отправлять заявку администратору
        return redirect('catalog')
