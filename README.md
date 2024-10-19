# Проект “Табло теннисного матча”

Веб-приложение, реализующее табло счёта теннисного матча.

[Тз проекта](https://zhukovsd.github.io/python-backend-learning-course/projects/tennis-scoreboard/)
![[Pasted image 20241019164744.png]]
## Функционал приложения
Приложение позволяет создавать, просматривать и редактировать теннисные матчи. Реализованы следующие функции:

- Создание нового матча
- Просмотр законченных матчей, поиск матчей по именам игроков
- Подсчёт очков в текущем матче
## Установка и запуск
1. Склонируйте репозиторий:
```
git clone https://github.com/EgorFurman/TennisMatchScoreboard.git
```

2. Установите MySQL на устройство и создайте базу данных для приложения(имя по умолчанию tennis_scoreboard)

3. Создайте виртуальное окружение:
- **На Windows**
    ```shell
     python -m venv venv
    ```
- **На MacOS/Linux**
    ```shell
	 python3.10 -m venv venv
    ```
	
4. Установите зависимости:
    ```shell
    pip install -r requirements.txt
    ```

5. Сконфигурируйте .env в соответствие с примером
```
	DB_DRIVER = mysql+pymysql
	DB_USER = your_username  # Ваше имя пользователя MySQL
	DB_PASSWORD = your_password  # Ваш пароль MySQL
	DB_HOST = localhost
	DB_PORT = 3306
	DB_NAME = tennis_scoreboard # Имя вашей базы данных
```

6. Запустите проект:
- **На Windows**
    ```shell
     python main.py
    ```
- **На MacOS/Linux**
    ```shell
     python3.10 main.py
    ```
## Стек
- python3.10 и выше
- waitress
- MySQL
- SQLAlchemy
- Jinja2
