# Интернет-магазин на Django

Данный проект представляет собой интернет-магазин, который включает: каталог товаров, корзину, оформление заказов, систему купонов, админ-панель для управления заказами, рассылку подтверждения заказа на email с помощью RabbitMQ и Celery. 

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/kabzal/online_shop.git
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate
    # Для Windows: venv\Scripts\activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Создайте файл `.env` в папке конфигурации online_shop/online_shop и добавьте необходимые переменные окружения:

    ```plaintext
    SECRET_KEY = 'your_secret_key'

    EMAIL_HOST_USER = 'username@domain.com'
    EMAIL_HOST_PASSWORD = 'your_email_host_password'
    ```

5. Запустите сервер разработки:

    ```bash
    cd online_shop
    python manage.py runserver
    ```

Проект будет доступен по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Запуск RabbitMQ и Celery

Для корректной работы всего функционала сайта (а именно рассылки подтверждений оформления заказов) необходимо запустить RabbitMQ и работника Celery.

Чтобы запустить RabbitMQ, необходимо установить его одним из способов, указанных по [ссылке](https://www.rabbitmq.com/docs/download) и открыть в браузере адрес [http://127.0.0.1:15672](http://127.0.0.1:15672/), где авторизоваться с логином и паролем `guest`.

Чтобы запустить работника Celery, воспользуйтесь следующей командой в терминале, находясь в папке проекта:
```bash
celery -A online_shop worker -l info
```
Если вы работаете на Windows, для корректной работы нужно будет запустить команду в следующем виде:
```bash
celery -A online_shop worker -l info -P eventlet
```
Теперь сайт может присылать уведомление об оформлении заказа на электронную почту.

