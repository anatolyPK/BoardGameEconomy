# BoardGame Economy API

BoardGame Economy API - это RESTful API на базе FastAPI для мониторинга и отслеживания финансовых операций, связанных с покупками и продажами настольных игр, а также получения основных статистических экономических показателей.

## Особенности

- Получение общих статиститческих данных об экономической составляющей настольных игр пользователя
- Получение списка всех транзакций
- Добавление новых транзакций
- Обновление сведений о транзакциях
- Удаление транзакций
- Поддержка аутентификации пользователя
- Информация об играх берется с BoardGameGeek
## Используемый стек

- [FastAPI](https://fastapi.tiangolo.com)
- [SQLAlchemy](https://www.sqlalchemy.org) 
- [Alembic](https://alembic.sqlalchemy.org) 
- [PostgreSQL](https://www.postgresql.org) 
- [Docker](https://www.docker.com) 
- [Ruff](https://docs.astral.sh/ruff/tutorial/) 

## Начало работы
### Запуск через Docker
1. Клонируйте репозиторий:

```bash
git clone https://https://github.com/anatolyPK/BoardGameEconomy.git
cd BoardGameEconomy
```

2. Создайте файл `.env` в корневом каталоге проекта и скопируйте в него все необходимые переменные окружения. Ниже представлены данные переменные:

```
#Переменные приложения FastAPI
DB_ECHO=1
DEBUG=1
PROJECT_NAME="BoardGameEconomy"
VERSION="0.0.1"
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Переменные для поключения к БД PostgreSQL
POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=db_port
```

3. Соберите Docker образ и запустите контейнер:

```bash
docker image build -t boardgame-economy-api .
docker run --name boardgame-economy -p 8001:8000 boardgame-economy-api
```


4. Создайте БД и внесите в файл .env переменные для подключения БД. Миграции применятся автоматически при первом запуске контейнера.


 API теперь будет доступен по адресу `http://localhost` на порту 8001.
 

### Установка без Docker

1. Клонируйте репозиторий и установите зависимости:

```
git clone https://https://github.com/anatolyPK/BoardGameEconomy.git
cd BoardGameEconomy
pip install -r requirements.txt
```
2. Выполните миграции базы данных с помощью Alembic:

```
alembic upgrade head
```
3. Запустите сервер


```
python main.py
```
API теперь будет доступен по адресу http://127.0.0.1:8000.

## Документация API

После запуска сервера разработки вы можете перейти по адресу http://127.0.0.1:8000/docs для доступа к автогенерированной интерактивной документации Swagger UI. 

Для доступа к документации ReDoc используйте http://127.0.0.1:8000/redoc.

