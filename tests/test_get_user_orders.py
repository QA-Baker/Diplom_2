import pytest
import allure
from test_data import valid_ingredients


class TestGetUserOrders:

    @allure.title("Получение заказов с авторизацией")
    @allure.description("Проверка успешного получения заказов авторизованного пользователя.")
    @pytest.mark.parametrize("ingredients", [valid_ingredients])
    def test_get_orders_with_auth(self, create_and_delete_user, base_url, ingredients, api_client):
        user_data, user_token, api_client = create_and_delete_user
        with allure.step("Установка заголовка авторизации"):
            api_client.headers.update({"Authorization": f"Bearer {user_token}"})

        with allure.step("Создание заказа для авторизованного пользователя"):
            order_data = {"ingredients": ingredients}
            api_client.post(f"{base_url}/orders", json=order_data)

        with allure.step("Получение заказов"):
            response = api_client.get(f"{base_url}/orders")

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response.json()['success'] is True
            assert len(response.json()['orders']) > 0

    @allure.title("Получение заказов без авторизации")
    @allure.description("Проверка ошибки при попытке получить заказы без авторизации.")
    def test_get_orders_without_auth(self, api_client, base_url):
        with allure.step("Удаление заголовка авторизации"):
            if "Authorization" in api_client.headers:
                del api_client.headers["Authorization"]

        with allure.step("Попытка получить заказы без авторизации"):
            response = api_client.get(f"{base_url}/orders")

        with allure.step("Проверка ошибки 401"):
            assert response.status_code == 401
            assert response.json()['message'] == "You should be authorised"
