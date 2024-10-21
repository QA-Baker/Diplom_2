import allure


class TestUpdateUser:

    @allure.title("Изменение email с авторизацией")
    @allure.description("Проверка успешного изменения email авторизованного пользователя.")
    def test_update_user_email_with_auth(self, create_and_delete_user, base_url, api_client):
        user_data, user_token, api_client = create_and_delete_user
        updated_email = {"email": "updated-email@yandex.ru"}

        with allure.step("Установка заголовка авторизации"):
            api_client.headers.update({"Authorization": f"Bearer {user_token}"})

        with allure.step("Изменение email"):
            response = api_client.patch(f"{base_url}/auth/user", json=updated_email)

        with allure.step("Проверка успешного изменения"):
            assert response.status_code == 200
            assert response.json()['user']['email'] == updated_email['email']

    @allure.title("Изменение имени с авторизацией")
    @allure.description("Проверка успешного изменения имени авторизованного пользователя.")
    def test_update_user_name_with_auth(self, create_and_delete_user, base_url, api_client):
        user_data, user_token, api_client = create_and_delete_user
        updated_name = {"name": "UpdatedName"}

        with allure.step("Установка заголовка авторизации"):
            api_client.headers.update({"Authorization": f"Bearer {user_token}"})

        with allure.step("Изменение имени"):
            response = api_client.patch(f"{base_url}/auth/user", json=updated_name)

        with allure.step("Проверка успешного изменения"):
            assert response.status_code == 200
            assert response.json()['user']['name'] == updated_name['name']

    @allure.title("Попытка изменения email на существующий")
    @allure.description("Проверка ошибки при попытке изменить email на существующий.")
    def test_update_user_with_existing_email(self, create_and_delete_user, base_url, api_client):
        user_data, user_token, api_client = create_and_delete_user

        with allure.step("Создание другого пользователя"):
            another_user_data = {"email": "existing-user@yandex.ru", "password": "password", "name": "ExistingUser"}
            api_client.post(f"{base_url}/auth/register", json=another_user_data)

        with allure.step("Попытка изменить email на существующий"):
            api_client.headers.update({"Authorization": f"Bearer {user_token}"})
            existing_email = {"email": "existing-user@yandex.ru"}
            response = api_client.patch(f"{base_url}/auth/user", json=existing_email)

        with allure.step("Проверка ошибки 403"):
            assert response.status_code == 403
            assert response.json()['message'] == "User with such email already exists"

    @allure.title("Изменение email без авторизации")
    @allure.description("Проверка ошибки при попытке изменить email без авторизации.")
    def test_update_user_email_without_auth(self, api_client, base_url):
        with allure.step("Удаление заголовка авторизации"):
            if "Authorization" in api_client.headers:
                del api_client.headers["Authorization"]

        with allure.step("Попытка изменить email без авторизации"):
            updated_email = {"email": "updated-email@yandex.ru"}
            response = api_client.patch(f"{base_url}/auth/user", json=updated_email)

        with allure.step("Проверка ошибки 401"):
            assert response.status_code == 401
            assert response.json()['message'] == "You should be authorised"

    @allure.title("Изменение имени без авторизации")
    @allure.description("Проверка ошибки при попытке изменить имя без авторизации.")
    def test_update_user_name_without_auth(self, api_client, base_url):
        with allure.step("Удаление заголовка авторизации"):
            if "Authorization" in api_client.headers:
                del api_client.headers["Authorization"]

        with allure.step("Попытка изменить имя без авторизации"):
            updated_name = {"name": "UpdatedName"}
            response = api_client.patch(f"{base_url}/auth/user", json=updated_name)

        with allure.step("Проверка ошибки 401"):
            assert response.status_code == 401
            assert response.json()['message'] == "You should be authorised"
