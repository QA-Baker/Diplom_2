# Параметры для теста с пропуском обязательных полей при создании пользователя
missing_user_fields = [
    "email",
    "password",
    "name"
]

# Неверные данные для логина
invalid_login_data = [
    {"email": "wrong-email@yandex.ru", "password": "password"},
    {"email": "test-temp@yandex.ru", "password": "wrongpassword"},
    {"email": "", "password": "password"},
    {"email": "test-temp@yandex.ru", "password": ""}
]

# Список ингредиентов для тестов
valid_ingredients = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
invalid_ingredients = ["invalid-hash-1", "invalid-hash-2"]
