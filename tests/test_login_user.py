import pytest
import allure
from test_data import invalid_login_data


class TestLoginUser:

    @allure.title("Авторизация существующего пользователя")
    @allure.description("Проверка успешной авторизации существующего пользователя.")
    def test_login_existing_user(self, create_and_delete_user, base_url, api_client):
        user_data, _, api_client = create_and_delete_user
        login_data = {"email": user_data['email'], "password": user_data['password']}

        with allure.step("Отправка запроса на авторизацию"):
            response = api_client.post(f"{base_url}/auth/login", json=login_data)

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response.json()['success'] is True

    @allure.title("Авторизация с неверными данными")
    @allure.description("Проверка ошибки при попытке авторизоваться с неверными логином или паролем.")
    @pytest.mark.parametrize("login_data", invalid_login_data)
    def test_login_with_invalid_data(self, api_client, login_data, base_url):
        with allure.step("Отправка запроса на авторизацию с неверными данными"):
            response = api_client.post(f"{base_url}/auth/login", json=login_data)

        with allure.step("Проверка ошибки 401"):
            assert response.status_code == 401
            assert response.json()['message'] == "email or password are incorrect"
