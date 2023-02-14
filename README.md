# Запуск docker-compose. Проект YaMDb

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
[![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://en.wikipedia.org/wiki/HTML5)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)

![example workflow](https://github.com/Abgrv/yamdb_final/actions/workflows/main.yml/badge.svg))

## Описание

Проект **YaMDb** собирает отзывы пользователей

## Установка

1. Проверить наличие Docker

   Прежде чем приступать к работе, убедиться что Docker установлен, для этого ввести команду:

   ```bash
   docker -v
   ```

   В случае отсутствия, скачать [Docker Desktop](https://www.docker.com/products/docker-desktop) 
для Mac или Windows. [Docker Compose](https://docs.docker.com/compose) будет установлен 
автоматически.

   В Linux проверить, что установлена последняя версия 
[Compose](https://docs.docker.com/compose/install/).

   Также можно воспользоваться официальной [инструкцией](https://docs.docker.com/engine/install/).

2. Клонировать репозиторий на локальный компьютер

   ```bash
   git clone https://github.com/egorcoders/infra_sp2.git
   ```

3. В корневой директории создать файл **.env**, согласно примеру:

   ```bash
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   ```

4. Запустить **docker-compose**

   Выполнить из корневой директории команду:

   ```bash
   docker-compose up -d
   ```

5. Заполнить БД

   Создать и выполнить миграции:

   ```bash
   docker-compose exec web python manage.py makemigrations --noinput
   docker-compose exec web python manage.py migrate --noinput
   ```

6. Подгрузить статику

   ```bash
   docker-compose exec web python manage.py collectstatic --no-input
   ```

7. Заполнить БД тестовыми данными

   Для заполнения базы использовать файл **fixtures.json**, в директории **infra_sp2**. Выполните 
команду:

   ```bash
   docker-compose exec web python manage.py dumpdata > fixtures.json
   ```

8. Создать суперпользователя

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

9. Остановить работу всех контейнеров

   ```bash
   docker-compose down
   ```

10. Пересобрать и запустить контейнеры

    ```bash
    docker-compose up -d --build
    ```

11. Мониторинг запущенных контейнеров

    ```bash
    docker stats
    ```

12. Остановить и удалить контейнеры, тома и образы

    ```bash
    docker-compose down -v
    ```

## Документация API YaMDb

Документация по использованию приложения доступна по эндпойнту: http://localhost/redoc/