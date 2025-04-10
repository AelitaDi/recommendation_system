
# Film Recommendation System
Этот проект представляет собой систему рекомендаций фильмов на основе двух алгоритмов: k-nearest-neighbours, PageRank. Проект включает:

-   **API**  для управления пользователями, фильмами, режиссерами, актерами, жанрами и взаимодействиями (оценками пользователей).
    
-   **Веб-интерфейс**  для просмотра и управления данными.
***
## Установка и запуск
### 1. Требования

-   Python 3.11+
    
-   Redis (для кэширования)
    
-   PostgreSQL (как основная база данных)
    
-   Установленные зависимости из  `requirements.txt`
### 2. Установка зависимостей

1.  Создайте виртуальное окружение:
	```
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
	```
2.  Установите зависимости:
	```
    pip install -r requirements.txt
	```
### 3. Настройка Redis
1. Установите Redis (если ещё не установлен):

	- **Linux**:  `sudo apt install redis`
	- **Mac**:  `brew install redis`
	- **Windows**: Скачайте с  [официального сайта](https://redis.io/download).
2. Запустите Redis:
	```
	redis-server.exe
	```
### 4. Подключение БД и Redis
1.  Создайте файл **.env** и заполните его по образцу **.env.sample**:
	```
    SECRET_KEY=django-insecure-12345!abcde67890!@#qwerty
    
    POSTGRES_DB=films_db
    POSTGRES_USER=films_user
    POSTGRES_PASSWORD=your_password
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    
    LOCATION=redis://localhost:6379/0
	```
2. Примените миграции:
	```
	python manage.py migrate
	```
## Добавление тестовых данных
1. Запустите **!важно!** `generate_test_data`:
	```
	python manage.py generate_test_data
	```
	**Внимание!** `generate_test_data` удаляет старые записи, будьте внимательны
	
2. Создайте суперпользователя:
	```
	python manage.py csu
	```
 	username: admin@example.com
	password: admin
3. Запустите проект:
	```
	python manage.py runserver
	```
4. Используйте административную панель Django (`http://127.0.0.1:8000/admin/`) для добавления:
	-   Пользователей
	-   Фильмов
	-   Режиссеров
	-   Жанров
    -   Актеров
    -   Оценок
5. Все данные о выданных рекомендациях сохраняются в базу данных для дальнейшего анализа.

## Использование API
Ознакомиться можно здесь:`http://127.0.0.1:8000/swagger/`

## Использование веб-интерфейса
1. **Главная страница** `http://127.0.0.1:8000/`
	- Здесь вы найдете все необходимые разделы
## Дополнительно
Чтобы увидеть полученный граф, выполните команду:
	```
	python visualization.py
	```
## Авторы
[Rogova U.](https://github.com/AelitaDi)