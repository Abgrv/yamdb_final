# Запуск docker-compose. Проект YaMDb

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
[![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://en.wikipedia.org/wiki/HTML5)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
![example workflow](https://github.com/Abgrv/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Описание

Проект **YaMDb** собирает отзывы пользователей

# Инструкция по развёртыванию.

## Локально:

1. Загрузите проект:
```
git@github.com:Abgrv/yamdb_final.git
```
2. Установите и активируйте виртуальное окружение:

```
python -m venv venv
source venv/Scripts/activate
python3 -m pip install --upgrade pip
```
3. Установите зависимости:
```
pip install -r requirements.txt
```
4. Выполнитe миграции:
```
python api_yamdb/manage.py migrate 
```
5. В папке с файлом manage.py выполните команду запуска:
```
python3 manage.py runserver
```

## Настройка Workflow и состоит из четрыех шагов:

- Проверка кода на соответствие PEP8
- Сборка и публикация образа бекенда на DockerHub.
- Автоматический деплой на удаленный сервер.
- Отправка уведомления в телеграм-чат.

## Описание команд для запуска приложения в контейнерах:

1. На Гитхабе добавьте данные в Settings - Secrets - Actions secrets:

```
DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub
HOST - ip-адрес сервера
USER - пользователь
SSH_KEY - приватный ssh-ключ
PASSPHRASE - кодовая фраза для ssh-ключа
SECRET_KEY - секретный ключ приложения django
TELEGRAM_TO - id своего телеграм-аккаунта
TELEGRAM_TOKEN - токен бота
DB_NAME - postgres (по умолчанию)
DB_ENGINE - django.db.backends.postgresql
DB_HOST - db (по умолчанию)
DB_PORT - 5432 (по умолчанию)
POSTGRES_USER - postgres (по умолчанию)
POSTGRES_PASSWORD - postgres (по умолчанию)
```

2. На сервере остановите службу nginx:

```
sudo systemctl stop nginx 
```

3. Установите docker и docker-compose:

```
sudo apt install docker.io
sudo apt install docker-compose -y
```

Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.

4. После успешного деплоя:

Для остановки контейнеров, выполните docker-compose down -v.

- Запуск контейнера.

- Применить миграции.

- Создать суперпользователя.

- Собрать статику.

```
sudo docker-compose up -d --build
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
```

Открываем браузер, вводим в адресную строку <ip_address_вашего_сервера>/api/v1/. Чтобы посмотреть на запущенный сервер перейдите по адресу 158.160.6.193/api/v1/

## Документация API YaMDb

Документация по использованию приложения доступна по эндпойнту: http://localhost/redoc/
