from celery import shared_task
from django.core.mail import send_mail
from .models import Order


# Задание: отправка письма об успешном размещении заказа
@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Заказ № {order.id}'
    message = f'Дорогой/Дорогая {order.first_name},\n\n' \
              f'Вы успешно разместили заказ. Номер' \
              f' вашего заказа: {order.id}'
    mail_send = send_mail(subject, message,
                          'kot-enot-online-shop@yandex.ru',
                          [order.email])
    return mail_send
