from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from cart.forms import CartAddProductForm
from .models import Category, Product


# Каталог товаров
class ProductList(ListView):
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # Если передан слаг, по нему из БД получаем категорию и сохраняем в контекст
        if self.kwargs.get('category_slug'):
            context['category'] = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        else:
            context['category'] = None
        return context

    def get_queryset(self):
        # Если в запросе есть слаг категории, то выдаем товары этой категории
        if self.kwargs.get('category_slug'):
            category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
            return Product.objects.filter(available=True, category=category)
        return Product.objects.filter(available=True)


# Карточка товара
class ProductDetail(DetailView):
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    extra_context = {
        'cart_product_form': CartAddProductForm(),
    }

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product,
                                 id=id,
                                 slug=slug,
                                 available=True)


# Обработка ошибки 404
def page_not_found(request, exception):
    return render(request,
                  'shop/page_not_found.html')