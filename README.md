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
```
/docs
```
или тут
```
[wArah cat_charity_fund Documentation](https://github.com/wArahh/cat_charity_fund/blob/master/openapi.json).
```


## Стек
- Python 3.9
- FastApi 0.78.0
- fastapi-users[sqlalchemy] 10.0.4
- SQLAlchemy 1.4.36
## Автор
- [Макаренко Никита](https://github.com/wArahh)
