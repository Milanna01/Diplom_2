import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import allure
import requests
import pytest
import urls
from helpers import generate_user_data


@allure.feature("Создание пользователя")
class TestUserRegistration:
    
    @allure.title("Успешное создание пользователя")
    def test_create_user_success(self):
        """Создание пользователя с валидными данными"""
        payload = generate_user_data()
        
        with allure.step("Выполнить POST запрос для регистрации пользователя"):
            response = requests.post(urls.Endpoints.register, json=payload)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert response_data['user']['email'] == payload['email']
        assert response_data['user']['name'] == payload['name']
        
        # Удаляем пользователя
        token = response_data['accessToken']
        delete_response = requests.delete(
            urls.Endpoints.user_delete,
            headers={'Authorization': f'Bearer {token}'}
        )
        assert delete_response.status_code == 200

    @allure.title("Создание пользователя с существующим email")
    def test_create_user_with_existing_email(self, authenticated_user):
        """Попытка создания пользователя с email, который уже используется"""
        existing_email = authenticated_user['email']
        payload = {
            'email': existing_email,
            'password': 'DifferentPassword123',
            'name': 'Different Name'
        }
        
        with allure.step("Выполнить POST запрос для регистрации пользователя с существующим email"):
            response = requests.post(urls.Endpoints.register, json=payload)
        
        assert response.status_code == 403
        assert response.json()['success'] is False

    @allure.title("Создание пользователя без обязательных полей")
    @pytest.mark.parametrize('payload, missing_field', [
        ({'password': 'password123', 'name': 'Test Name'}, 'email'),
        ({'email': 'test@example.com', 'name': 'Test Name'}, 'password'),
        ({'email': 'test@example.com', 'password': 'password123'}, 'name'),
    ])
    def test_create_user_missing_field(self, payload, missing_field):
        """Создание пользователя без обязательного поля"""
        with allure.step(f"Выполнить POST запрос без поля {missing_field}"):
            response = requests.post(urls.Endpoints.register, json=payload)
        
        with allure.step(f"Проверить ошибку при отсутствии поля {missing_field}"):
            # Исправлено: однозначный ожидаемый результат - 400 Bad Request
            assert response.status_code == 400
        
        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()['success'] is False