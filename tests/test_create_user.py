import pytest
import allure
from test_data import missing_user_fields


class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    @allure.description("Проверка успешного создания уникального пользователя.")
    def test_create_unique_user(self, create_and_delete_user):
        user_data, user_token, api_client = create_and_delete_user
        with allure.step("Проверка, что пользователь был успешно создан"):
            assert user_token is not None, f"User token is None, response: {user_data}"

    @allure.title("Создание уже существующего пользователя")
    @allure.description("Проверка попытки создания пользователя с данными, которые уже существуют.")
    def test_create_existing_user(self, create_and_delete_user, base_url, api_client):
        user_data, _, api_client = create_and_delete_user
        with allure.step("Попытка создать пользователя с существующими данными"):
            response = api_client.post(f"{base_url}/auth/register", json=user_data)

        with allure.step("Проверка ошибки 403"):
            assert response.status_code == 403

    @allure.title("Создание пользователя без обязательных полей")
    @allure.description("Проверка ошибки при создании пользователя с пропуском одного из обязательных полей.")
    @pytest.mark.parametrize("missing_field", missing_user_fields)
    def test_create_user_with_missing_fields(self, api_client, missing_field, base_url):
        user_data = {"email": "test-unique@yandex.ru", "password": "password", "name": "TestUser"}
        user_data.pop(missing_field)

        with allure.step(f"Попытка создать пользователя без поля {missing_field}"):
            response = api_client.post(f"{base_url}/auth/register", json=user_data)

        with allure.step("Проверка ошибки 403"):
            assert response.status_code == 403
            assert response.json()['message'] == "Email, password and name are required fields"
