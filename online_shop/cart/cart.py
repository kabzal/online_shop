from django.conf import settings
from decimal import Decimal

from shop.models import Product
from coupons.models import Coupon


# Класс для создания корзин
class Cart:
    def __init__(self, request):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        """
         Добавить товар в корзину либо обновить его количество.
         """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # пометить сеанс как "измененный",
        # чтобы обеспечить его сохранение
        self.session.modified = True

    def remove(self, product):
        """
        Удалить товар из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # Получить полную стоимость корзины
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # Очистит корзину
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    # Свойство: купон
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    # Вычисление скидки по купону
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) \
                    * self.get_total_price()
        return Decimal(0)

    # Получение полной стоимости корзины с учетом скидки
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()