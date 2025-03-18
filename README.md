# Tennis Match Scoreboard

Приложение для отслеживания счета в теннисном матче, разработанное на Python.  
Проект создан в рамках курса по развитию своих профессиональных навыков https://zhukovsd.github.io/python-backend-learning-course/  
ТЗ проекта: https://zhukovsd.github.io/python-backend-learning-course/projects/tennis-scoreboard/

## Описание

Tennis Match Scoreboard - это простое приложение, которое позволяет отслеживать счет теннисного матча между двумя игроками. Приложение реализует стандартную систему подсчета очков в теннисе (поинты, геймы, сеты).

## Функциональные возможности

- Создание матча с указанием имен игроков
- Отслеживание счета (поинты, геймы, сеты)
- Зачисление очка соответствующему игроку при нажатии на кнопку
- Автоматический подсчет очков в соответствии с правилами тенниса

## Технический стек

- Python 3.8+
- SQLAlchemy для работы с базой данных
- MySQL в качестве СУБД
- Alembic для миграций базы данных
- Jinja2 для шаблонизации
- Waitress для запуска веб-сервера

## Требования

- Python 3.8 или выше
- Установленный pip (менеджер пакетов Python)
- MySQL сервер (5.7 или выше)
- Виртуальное окружение (опционально, но рекомендуется)

## Установка

1. Клонируйте репозиторий из папки на вашем компьютере в которой должен находится проект:
   ```bash
   git clone https://github.com/Gichie/tennis_match_csoreboard_v_2.git
   cd tennis_match_csoreboard_v_2
   ```

2. Создайте и активируйте виртуальное окружение (опционально):
   ```bash
   # Для Windows
   python -m venv venv
   venv\Scripts\activate

   # Для Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -e .
   ```

4. Для разработки установите дополнительные зависимости:
   ```bash
   pip install -e ".[dev]"
   ```
   
   Для запуска тестов установите дополнительные зависимости:
   ```bash
   pip install -e ".[test]"
   ```

5. Настройте переменные окружения:
   - Создайте файл `.env` в корневой директории проекта
   - Укажите следующие переменные окружения:
     ```
     DB_USER=your_database_username
     DB_PASSWORD=your_database_password
     DB_HOST=database_host_address
     DB_NAME=database_name
     DB_PORT=database_port
     ```
   - Замените значения на актуальные для вашей базы данных

## Настройка базы данных MySQL

1. Установите MySQL, если он еще не установлен.

3. Создайте базу данных для приложения:
   ```sql
   CREATE DATABASE tennis_scoreboard;
   CREATE USER 'tennis_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON tennis_scoreboard.* TO 'tennis_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```
   
4. Обновите файл `.env` с созданными учетными данными:
   ```
   DB_USER=tennis_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_NAME=tennis_scoreboard
   DB_PORT=3306
   ```

5. Выполните миграции базы данных:
   ```bash
   alembic upgrade head
   ```

## Запуск приложения

1. После установки и настройки выполните:
   ```bash
   python -m main
   ```

2. Откройте браузер и перейдите по адресу `http://localhost:8000`

## Разработка

- Для запуска тестов:
  ```bash
  pytest
  ```

- Для проверки кода:
  ```bash
  ruff check .
  mypy .
  ```

## Контакты

- Автор: Gichie
- Email: kksenys@gmail.com
- GitHub: https://github.com/Gichie/tennis_match_csoreboard_v_2