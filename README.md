## Ссылка на проверку проекта:
84.201.167.114/

Админ панель:
логин: miha
пароль: 1
```
http://84.201.167.114/admin/
```

## Описание
Приложение для публикации, поиска и выбора кулинарных рецептов. Каждый может авторизоваться,
выложить свои рецепты, а так же подписаться на чужие обновления, сформироваться список своих
любимых рецептов и сформировать список покупок.


## Схема наполнения файла .env проекта Infra_sp2
Файл необходимо разместить в директории foodgram-project-react/infra/

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=************** # Секретный ключ вашего проекта
```

## Техническое описание проекта Infra_sp2

Для запуска проекта необходимо клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/RussianPostman/foodgram-project-react
cd infra
docker-compose up -d --build
docker-compose exec backend python manage.py makemigrations app
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py load_data
```
Перейти в браузере по адресу
```
http://127.0.0.1/signup
```
## Документация

К проекту по адресу
```
http://127.0.0.1/redoc/
```
подключена документация foodgram-project-react. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.