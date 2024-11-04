# Параметры для теста с пропуском обязательных полей при создании пользователя
MISSING_USER_FIELDS = [
    "email",
    "password",
    "name"
]

# Неверные данные для логина
INVALID_LOGIN_DATA = [
    {"email": "wrong-email@yandex.ru", "password": "password"},
    {"email": "test-temp@yandex.ru", "password": "wrongpassword"},
    {"email": "", "password": "password"},
    {"email": "test-temp@yandex.ru", "password": ""}
]

# Список ингредиентов для тестов
VALID_INGREDIENTS = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
INVALID_INGREDIENTS = ["invalid-hash-1", "invalid-hash-2"]

# Сообщения об ошибках
ERROR_MSG_INGREDIENT_IDS_REQUIRED = "Ingredient ids must be provided"
ERROR_MSG_INTERNAL_SERVER_ERROR = "Internal Server Error"
ERROR_MSG_EMAIL_ALREADY_EXISTS = "User with such email already exists"
ERROR_MSG_AUTH_REQUIRED = "You should be authorised"
ERROR_MSG_INVALID_LOGIN = "email or password are incorrect"
ERROR_MSG_MISSING_USER_FIELDS = "Email, password and name are required fields"
