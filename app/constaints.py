GET_OBJECT_ERROR = 'Во время вызова таблицы {model} проищошла ошибка: {error}'
DB_CHANGE_ERROR = (
    'При попытке изменения таблицы {model} '
    'в базе данных произошла ошибка: {error}'
)
NOT_IN_DB = 'Объект не найден в базе данных'
NAME_ALREADY_IN_USE = 'Это название уже занято'
CANNOT_DELETE_INVESTED_PROJECT = (
    'Нельзя удалять закрытый проект или проект, '
    'в который уже были инвестированы средства.'
)
CANT_SET_LESS_THAN_ALREADY_DONATED = (
    'Нельзя изменить поле full_amount на значение меньше уже полученного'
)
BEARER_TOKEN_URL = 'auth/jwt/login'
JWT_LIFETIME = 3600
AUTHENTICATION_BACKEND_NAME = 'jwt'
