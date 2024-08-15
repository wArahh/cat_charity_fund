# Кошачий благотворительный фонд (0.1.0)
## Команды развертывания
Клонируйте репозиторий к себе на компьютер при помощи команды:
```
git clone git@github.com:wArahh/cat_charity_fund.git
```

Создайте, активируйте виртуальное окружение и установите зависимости:
```
cd cat_charity_fund/
```
```
python -m venv venv
```
```
pip install -r requirements.txt
```
### создайте .env файл по примеру:
```
TITLE='Кошачий благотворительный фонд (0.1.0)'
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET='SECRET'
```
### активируйте базу данных командой:
```
alembic upgrade head
```
### запустите проект командой
```
uvicorn app.main:app --reload
```
### Документацию вы можете посмотреть по адресу
[Swagger](http://127.0.0.1:8000/docs)

или тут

[ReDoc](http://127.0.0.1:8000/redoc)



## Стек
- Python
- FastApi
- fastapi-users[sqlalchemy] 
- SQLAlchemy
## Автор
- [Макаренко Никита](https://github.com/wArahh)
