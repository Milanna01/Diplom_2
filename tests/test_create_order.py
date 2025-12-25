import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import allure
import requests
import urls


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, authenticated_user, available_ingredients):
        headers = {'Authorization': f'Bearer {authenticated_user["token"]}'}
        ingredients = available_ingredients[:2] if available_ingredients else []
        
        with allure.step("Выполнить POST запрос для создания заказа с авторизацией"):
            response = requests.post(
                urls.Endpoints.create_order,  # используем create_order вместо ORDERS
                json={'ingredients': ingredients},
                headers=headers
            )
        
        with allure.step("Проверить статус код и успешность ответа"):
            assert response.status_code == 200
            assert response.json()['success'] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, available_ingredients):
        ingredients = available_ingredients[:2] if available_ingredients else []
        
        with allure.step("Выполнить POST запрос для создания заказа без авторизации"):
            response = requests.post(
                urls.Endpoints.create_order,  # используем create_order вместо ORDERS
                json={'ingredients': ingredients}
            )
        
        with allure.step("Проверить статус код и сообщение об ошибке авторизации"):
            assert response.status_code == 401
            assert response.json()['success'] is False

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, authenticated_user, available_ingredients):
        headers = {'Authorization': f'Bearer {authenticated_user["token"]}'}
        ingredients = available_ingredients[:3] if available_ingredients else []
        
        with allure.step("Выполнить POST запрос для создания заказа с ингредиентами"):
            response = requests.post(
                urls.Endpoints.create_order,  # используем create_order вместо ORDERS
                json={'ingredients': ingredients},
                headers=headers
            )
        
        with allure.step("Проверить статус код и успешность ответа"):
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, authenticated_user):
        headers = {'Authorization': f'Bearer {authenticated_user["token"]}'}
        
        with allure.step("Выполнить POST запрос для создания заказа без ингредиентов"):
            response = requests.post(
                urls.Endpoints.create_order,  # используем create_order вместо ORDERS
                json={'ingredients': []},
                headers=headers
            )
        
        with allure.step("Проверить статус код и сообщение об ошибке валидации"):
            assert response.status_code == 400
            assert response.json()['success'] is False

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_hash(self, authenticated_user):
        headers = {'Authorization': f'Bearer {authenticated_user["token"]}'}
        
        with allure.step("Выполнить POST запрос для создания заказа с неверным хешем ингредиентов"):
            response = requests.post(
                urls.Endpoints.create_order,  # используем create_order вместо ORDERS
                json={'ingredients': ['invalid_hash_1', 'invalid_hash_2']},
                headers=headers
            )
        
        with allure.step("Проверить статус код 500 и неуспешность ответа"):
            # Уточняем ожидаемый статус код: по логике приложения при неверном хеше должен быть 500
            assert response.status_code == 500
            assert response.json()['success'] is False