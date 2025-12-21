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
        
        response = requests.post(
            urls.Endpoints.create_order,  # используем create_order вместо ORDERS
            json={'ingredients': ingredients},
            headers=headers
        )
        
        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, available_ingredients):
        ingredients = available_ingredients[:2] if available_ingredients else []
        
        response = requests.post(
            urls.Endpoints.create_order,  # используем create_order вместо ORDERS
            json={'ingredients': ingredients}
        )
        
        assert response.status_code == 401
        assert response.json()['success'] is False

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, authenticated_user, available_ingredients):
        headers = {'Authorization': f'Bearer {authenticated_user["token"]}'}
        ingredients = available_ingredients[:3] if available_ingredients else []
        
        response = requests.post(
            urls.Endpoints.create_order,  # используем create_order вместо ORDERS
            json={'ingredients': ingredients},
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, authenticated_user):
        headers = {'Authorization': f'Bearer {authenticated_user["token"]}'}
        
        response = requests.post(
            urls.Endpoints.create_order,  # используем create_order вместо ORDERS
            json={'ingredients': []},
            headers=headers
        )
        
        assert response.status_code == 400
        assert response.json()['success'] is False

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_hash(self, authenticated_user):
        headers = {'Authorization': f'Bearer {authenticated_user["token"]}'}
        
        response = requests.post(
            urls.Endpoints.create_order,  # используем create_order вместо ORDERS
            json={'ingredients': ['invalid_hash_1', 'invalid_hash_2']},
            headers=headers
        )
        
        assert response.status_code in [400, 500]
        assert response.json()['success'] is False