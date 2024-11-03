import pytest
import allure
from test_data import VALID_INGREDIENTS, INVALID_INGREDIENTS, ERROR_MSG_INGREDIENT_IDS_REQUIRED, \
    ERROR_MSG_INTERNAL_SERVER_ERROR


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    @allure.description("Проверка создания заказа авторизованным пользователем с валидными ингредиентами.")
    @pytest.mark.parametrize("ingredients", [VALID_INGREDIENTS])
    def test_create_order_with_auth(self, create_and_delete_user, base_url, ingredients, api_client):
        user_data, user_token, api_client = create_and_delete_user
        with allure.step("Установка заголовка авторизации"):
            api_client.headers.update({"Authorization": f"Bearer {user_token}"})

        with allure.step("Создание заказа"):
            order_data = {"ingredients": ingredients}
            response = api_client.post(f"{base_url}/orders", json=order_data)

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response.json()['success'] is True

    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверка создания заказа без авторизации с валидными ингредиентами.")
    @pytest.mark.parametrize("ingredients", [VALID_INGREDIENTS])
    def test_create_order_without_auth(self, api_client, base_url, ingredients):
        with allure.step("Удаление заголовка авторизации"):
            if "Authorization" in api_client.headers:
                del api_client.headers["Authorization"]

        with allure.step("Создание заказа без авторизации"):
            order_data = {"ingredients": ingredients}
            response = api_client.post(f"{base_url}/orders", json=order_data)

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response.json()['success'] is True

    @allure.title("Создание заказа без ингредиентов с авторизацией")
    @allure.description("Проверка ошибки при создании заказа без ингредиентов с авторизацией.")
    def test_create_order_without_ingredients(self, create_and_delete_user, base_url, api_client):
        user_data, user_token, api_client = create_and_delete_user
        with allure.step("Установка заголовка авторизации"):
            api_client.headers.update({"Authorization": f"Bearer {user_token}"})

        with allure.step("Попытка создать заказ без ингредиентов"):
            order_data = {"ingredients": []}
            response = api_client.post(f"{base_url}/orders", json=order_data)

        with allure.step("Проверка ошибки 400"):
            assert response.status_code == 400
            assert response.json()['message'] == ERROR_MSG_INGREDIENT_IDS_REQUIRED

    @allure.title("Создание заказа без ингредиентов без авторизации")
    @allure.description("Проверка ошибки при создании заказа без ингредиентов и без авторизации.")
    def test_create_order_without_ingredients_without_auth(self, api_client, base_url):
        with allure.step("Удаление заголовка авторизации"):
            if "Authorization" in api_client.headers:
                del api_client.headers["Authorization"]

        with allure.step("Попытка создать заказ без ингредиентов без авторизации"):
            order_data = {"ingredients": []}
            response = api_client.post(f"{base_url}/orders", json=order_data)

        with allure.step("Проверка ошибки 400"):
            assert response.status_code == 400
            assert response.json()['message'] == ERROR_MSG_INGREDIENT_IDS_REQUIRED

    @allure.title("Создание заказа с неверными хешами ингредиентов")
    @allure.description("Проверка ошибки 500 при создании заказа с неверными хешами ингредиентов.")
    @pytest.mark.parametrize("ingredients", [INVALID_INGREDIENTS])
    def test_create_order_with_invalid_ingredient_hash(self, create_and_delete_user, base_url, ingredients, api_client):
        user_data, user_token, api_client = create_and_delete_user
        with allure.step("Установка заголовка авторизации"):
            api_client.headers.update({"Authorization": f"Bearer {user_token}"})

        with allure.step("Попытка создать заказ с неверными хешами ингредиентов"):
            order_data = {"ingredients": ingredients}
            response = api_client.post(f"{base_url}/orders", json=order_data)

        with allure.step("Проверка ошибки 500"):
            assert response.status_code == 500
            try:
                error_message = response.json().get('message')
                assert error_message == ERROR_MSG_INTERNAL_SERVER_ERROR
            except ValueError:
                assert "Internal Server Error" in response.text
