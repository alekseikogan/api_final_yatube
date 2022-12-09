# Финальное задание 9-го спринта
## Проект «API для Yatube»
### 1. Описание проекта
Что это за проект, какую задачу он решает, в чём его польза? 
Давайте разбираться.

### 2. Как запустить проект:
Как развернуть проект на локальной машине
- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/alekseikogan/api_final_yatube.git
```

```
cd api_final_yatube
```

- Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

- Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

- Выполнить миграции:

```
python manage.py migrate
```

- Запустить проект:

```
python manage.py runserver
```
### 3. Некоторые примеры запросов к API. 
