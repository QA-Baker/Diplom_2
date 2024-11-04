import pytest
import requests

# Базовый URL для всех запросов к API
BASE_URL = "https://stellarburgers.nomoreparties.site/api"


@pytest.fixture(scope='session')
def api_client():
    # Фикстура для создания сессии HTTP клиента
    return requests.Session()


@pytest.fixture(scope='session')
def base_url():
    # Фикстура для передачи базового URL в тесты
    return BASE_URL


@pytest.fixture(scope='function')
def create_and_delete_user(api_client, base_url):
    # Фикстура для создания и удаления пользователя перед/после теста
    # Создание тестового пользователя
    user_data = {
        "email": "test-temp@yandex.ru",
        "password": "password",
        "name": "TempUser"
    }
    response = api_client.post(f"{base_url}/auth/register", json=user_data)

    # Извлечение токена и удаление префикса "Bearer "
    user_token = response.json().get('accessToken', '').split(' ')[1] if response.status_code == 200 else None

    yield user_data, user_token, api_client  # Передача данных в тест

    # Удаление пользователя после теста
    if user_token:
        api_client.headers.update({"Authorization": f"Bearer {user_token}"})
        api_client.delete(f"{base_url}/auth/user")
