# DDD Kafka Python

Современное приложение на Python, построенное с использованием принципов Domain-Driven Design (DDD), FastAPI и MongoDB.

## 🚀 Особенности

- **DDD архитектура** - Чистая архитектура с разделением на слои
- **FastAPI** - Современный асинхронный веб-фреймворк
- **MongoDB** - NoSQL база данных с async драйвером Motor
- **Docker & Docker Compose** - Контейнеризированная среда разработки
- **Poetry** - Современное управление зависимостями Python
- **Pre-commit хуки** - Автоматическая проверка кода перед коммитом
- **Pytest** - Фреймворк для тестирования

## 📋 Требования

Перед началом работы убедитесь, что у вас установлено:

- [Docker](https://www.docker.com/get-started) и Docker Compose
- [Poetry](https://python-poetry.org/docs/#installation) (для локальной разработки)
- Python 3.11+ (для локальной разработки)

## 🛠️ Установка

### Использование Docker (Рекомендуется)

1. **Клонируйте репозиторий**

   ```bash
   git clone <repository-url>
   cd ddd-kafka-python
   ```

2. **Настройте переменные окружения**

   ```bash
   cp .env.example .env
   # Отредактируйте файл .env с вашими настройками
   ```

3. **Запустите приложение**

   ```bash
   make app
   ```

4. **Просмотр логов**

   ```bash
   make app-logs
   ```

### Локальная разработка

1. **Установите зависимости**

   ```bash
   poetry install
   ```

2. **Настройте интерпретатор Python в IDE**

   ```bash
   # Получите путь к виртуальному окружению
   poetry env activate
   ```
   
   Затем в VS Code:
   - Нажмите `Ctrl + Shift + P` (или `Cmd + Shift + P` на macOS)
   - Выберите `Python: Select Interpreter`
   - Выберите `Enter interpreter path...`
   - Скопируйте путь из команды выше и добавьте `/bin/python3` в конце
   
   Например: `/Users/user/Library/Caches/pypoetry/virtualenvs/ddd-kafka-python-xxx/bin/python3`

3. **Установите pre-commit хуки**

   ```bash
   pre-commit install
   ```

4. **Запустите сервер разработки**

   ```bash
   uvicorn app.application.api.main:create_app --factory --reload
   ```

## 🐳 Docker команды

Проект включает Makefile для упрощения работы с Docker:

```bash
make app               # Запустить приложение
make app-down          # Остановить приложение
make app-logs          # Просмотреть логи приложения
make app-shell         # Подключиться к контейнеру
make precommit         # Запустить pre-commit проверки
```

## 📁 Структура проекта

```
ddd-kafka-python/
├── app/                              # Основной код приложения
│   ├── application/                  # Слой приложения
│   │   ├── api/                     # API эндпоинты
│   │   │   ├── main.py              # Инициализация FastAPI
│   │   │   └── messages/            # Эндпоинты для сообщений
│   │   └── __init__.py
│   ├── domain/                       # Доменный слой
│   │   ├── entities/                # Доменные сущности
│   │   │   ├── base.py             # Базовая сущность
│   │   │   └── messages.py         # Сущности сообщений
│   │   ├── value_objects/          # Объекты-значения
│   │   │   ├── base.py
│   │   │   └── messages.py
│   │   ├── exceptions/              # Доменные исключения
│   │   │   ├── base.py
│   │   │   └── messages.py
│   │   └── __init__.py
│   ├── infra/                        # Инфраструктурный слой
│   │   └── __init__.py
│   ├── logic/                        # Бизнес-логика
│   │   └── __init__.py
│   └── tests/                        # Тесты
│       └── domain/
│           └── test_messages.py
├── docker_compose/                   # Конфигурации Docker Compose
│   └── app.yaml                     # Сервисы приложения
├── Dockerfile                        # Конфигурация Docker образа
├── Makefile                          # Команды для разработки
├── pyproject.toml                    # Конфигурация Poetry
├── poetry.lock                       # Зафиксированные версии зависимостей
└── README.md                         # Документация проекта
```

## 🏗️ DDD Архитектура

Проект следует принципам Domain-Driven Design:

### Слои приложения

1. **Domain (Домен)** - Ядро бизнес-логики
   - `entities/` - Доменные сущности с уникальными идентификаторами
   - `value_objects/` - Неизменяемые объекты-значения
   - `exceptions/` - Доменные исключения

2. **Application (Приложение)** - Слой координации
   - `api/` - REST API эндпоинты
   - Оркестрация use cases

3. **Infrastructure (Инфраструктура)** - Технические детали
   - Репозитории
   - Внешние сервисы
   - База данных

4. **Logic (Логика)** - Бизнес-логика и use cases

### Примеры сущностей

**MessageEntity** - Сообщение в чате
```python
@dataclass
class MessageEntity(BaseEntity):
    text: TextValueObject
```

**ChatEntity** - Чат с сообщениями
```python
@dataclass
class ChatEntity(BaseEntity):
    title: TitleValueObject
    messages: list[MessageEntity]
    
    def add_message(self, message: MessageEntity):
        self.messages.append(message)
```

## ⚙️ Конфигурация

### Переменные окружения

Приложение использует переменные окружения для конфигурации. Создайте файл `.env` со следующими переменными:

```env
# MongoDB
MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_DB=ddd_kafka_db
MONGO_USER=admin
MONGO_PASSWORD=password

# Application
APP_PORT=8000
DEBUG=True
```

## 🧪 Тестирование

Проект использует pytest для тестирования:

```bash
# Запуск всех тестов
poetry run pytest

# Запуск с подробным выводом
poetry run pytest -v

# Запуск конкретного теста
poetry run pytest app/tests/domain/test_messages.py
```

## 🎨 Качество кода

### Pre-commit хуки

Проект настроен с pre-commit для автоматической проверки кода:

```bash
# Установка хуков
pre-commit install

# Ручной запуск проверок
make precommit
```

### Isort

Автоматическая сортировка импортов настроена в `pyproject.toml`:
- Длина строки: 120 символов
- Multi-line вывод: 3
- Алфавитная сортировка в секциях

## 📚 API Документация

После запуска приложения, документация API доступна по адресу:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/redoc

## 🚀 Разработка

### Добавление новой сущности

1. Создайте value objects в `domain/value_objects/`
2. Создайте сущность в `domain/entities/`
3. Добавьте исключения в `domain/exceptions/`
4. Напишите тесты в `tests/domain/`
5. Реализуйте use cases в `logic/`
6. Создайте API эндпоинты в `application/api/`

### Структура теста

```python
from faker import Faker
from domain.entities.messages import MessageEntity
from domain.value_objects.messages import TextValueObject

def test_message_entity():
    faker = Faker()
    text = TextValueObject(faker.text())
    message = MessageEntity(text=text)
    assert message.text == text
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Запустите `make precommit`
6. Отправьте pull request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT - см. файл LICENSE для деталей.

## 🆘 Поддержка

Если у вас возникли проблемы или вопросы:

1. Проверьте [документацию FastAPI](https://fastapi.tiangolo.com/)
2. Просмотрите логи: `make app-logs`
3. Подключитесь к контейнеру: `make app-shell`

## 🔄 Обновления

Для обновления проекта:

1. Получите последние изменения
   ```bash
   git pull origin master
   ```

2. Обновите зависимости
   ```bash
   poetry update
   ```

3. Пересоберите контейнеры
   ```bash
   make app-down
   make app
   ```

---

**Удачной разработки!** 🎉
