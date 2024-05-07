# Кошачий благотворительный фонд

## Описание проекта
Данный проект представляет собой краудфандинговый сервис. 

Технологии
- Язык программирования: Python
- Фреймворк: FastAPI
- поддерживает асинхронность
- генерирует отчетность с использованием Google Drive и Google Sheets

## Установка и настройка
1. склонируйте репозиторий:

  ```
  git clone git@github.com:<ваше имя пользователя>/cat_charity_fund.git
  ```

2. создайте и активируйте виртуальное окружение:
* Для Linux/macOS

    ```
    source venv/bin/activate
    ```

* Для Windows

    ```
    source venv/scripts/activate
    ```
3. Обновите менеджер пакетов pip и установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
4. В корне проекта создайте файл в котором будете хранить переменные окружения, например `.env` и установите в нем следующие перемнные:
* `APP_TITLE=<название проекта>` - опционально;
* `DATABASE_URL=<параметры для подключения к БД>` - например: sqlite+aiosqlite:///./fastapi.db - обязательно для установки, в противном случае не получется применить миграции и создать необходимые таблицы;
* `SECRET=<секретное слово>` - для генерации токена пользователя;
* `FIRST_SUPERUSER_EMAIL=<email>` - опционально, для создания суперюзера при первом запуске проекта;
* `FIRST_SUPERUSER_PASSWORD=adminpassword` - опционально, для создания суперюзера при первом запуске проекта.

Создайте сервыисный аккаунт Google Cloud Platform. Получите ключ и JSON-файл с данными сервисного аккаунта, чтобы управлять подключёнными API из вашего Python-приложения и укажите эти данные в вашем .env.
* `TYPE=<type>`
* `PROJECT_ID=<project_id>`
* `PRIVATE_KEY_ID=<private_key_id>`
* `PRIVATE_KEY=<private_key>`
* `CLIENT_EMAIL=<client_email>`
* `CLIENT_ID=<client_id>`
* `AUTH_URI=<auth_uri>`
* `TOKEN_URI=<token_uri>`
* `AUTH_PROVIDER_X509_CERT_URL=<auth_provider_x509_url>`
* `CLIENT_X509_CERT_URL=<client_x509_cert_url>`
* `EMAIL=<ваш_gmail`

** данные переменные можно заполнить непосредственно в `class Config(BaseConfig)`, кроме `DATABASE_URL`, но помните что подобное хранение секретов не безопасно, создатели проекта рекомендую хранить секреты в переменных окружения.

5. Примените миграции и запустите приложение:
   ```
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

## Использование
### /charity_project/:
* Чтобы получить все благотварительные проекты необхоодимо отправить get-запрос по адресу: `http://127.0.0.1:8000/charity_project/` - доступно абсолютно любому пользователю. Пример ответа:
  ```json
  [
    {
      "name": "string",
      "description": "string",
      "full_amount": 0,
      "create_date": "2024-01-28T03:45:52.682Z",
      "id": 0,
      "invested_amount": 0,
      "fully_invested": true,
      "close_date": "2024-01-28T03:45:52.682Z"
    }
  ]
  ```
* Создание, редактирование и удаление благотварительных проектов доступно только суперпользователю.
* Изменение и удаление закрытых проектов запрещено.
* Как только создается новый благотварительный проект нераспределенные пожертвования автоматически поступят в него в пределах необходимой суммы.

### /donation/:
* Доступно только зарегистрированным пользователям и суперпользователям
* Изменение пожертвования запрещено
* Также пользователям доступен просмотр всех своих пожертвования по адресу: `http://127.0.0.1:800/donation/my/`. Пример ответа:
  ```json
  [
    {
      "full_amount": 0,
      "comment": "string",
      "id": 0,
      "create_date": "2024-01-28T05:17:35.741Z"
    }
  ]
  ```
* Доступ ко всем пожертвованиям всех пользователей доступен только суперюзеру. Также суперюзеру доступны вся информация о пожертвованиях:
  ```json
  [
    {
      "full_amount": 0,
      "comment": "string",
      "id": 0,
      "create_date": "2024-01-28T05:50:37.965Z",
      "user_id": 0,
      "invested_amount": 0,
      "fully_invested": true,
      "close_date": "2024-01-28T05:50:37.965Z"
    }
  ]
  ```

### /users/:
* Просмотр и изменение пользователя

### /auth/:
* Регистрация и авторизация пользователя.

### /google/:
* Получение администратором отчета по закрытым проектам.
```json
  [
    {
      "name": "string",
      "duration": "1 day, 0:34:59.516646",
      "description": "string"
    }
  ]
  ```

Более подробно с эндпоинтами можно ознакомиться в интерактивной документации после запуска проекта:
* [ReDoc](http://127.0.0.1:8000/docs)
* [Swagger](http://127.0.0.1:800/redoc)
  
