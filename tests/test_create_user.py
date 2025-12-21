import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import allure
import requests
import pytest
import urls
from generators import generate_email, generate_password, generate_name


class TestUserRegistration:
    @allure.title('Создание пользователя')
    def test_create_user_success(self, new_user_data):
        """Создание пользователя с валидными данными"""
        payload = new_user_data
        
        with allure.step('Создание пользователя'):
            response = requests.post(urls.Endpoints.register, json=payload)  # используем register вместо REGISTER
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert response_data['user']['email'] == payload['email']
        assert response_data['user']['name'] == payload['name']
        
        # Удаляем пользователя
        token = response_data['accessToken']
        requests.delete(
            urls.Endpoints.user_delete,  # используем user_delete вместо USER
            headers={'Authorization': f'Bearer {token}'}
        )

    @allure.title('Создание уже существующего пользователя')
    def test_create_existing_user(self):
        """Создание пользователя с уже существующим email"""
        user_data = {
            'email': generate_email(),
            'password': generate_password(),
            'name': generate_name()
        }
        
        # Регистрируем первого пользователя
        first_response = requests.post(urls.Endpoints.register, json=user_data)  # используем register
        assert first_response.status_code == 200
        token = first_response.json()['accessToken']
        
        # Пытаемся зарегистрировать с тем же email
        response = requests.post(urls.Endpoints.register, json=user_data)  # используем register
        
        assert response.status_code == 403
        assert response.json()['success'] is False
        
        # Удаляем пользователя
        requests.delete(
            urls.Endpoints.user_delete,  # используем user_delete
            headers={'Authorization': f'Bearer {token}'}
        )

    @allure.title('Создание пользователя без указания одного из полей')
    @pytest.mark.parametrize('payload', [
        {'password': 'password123', 'name': 'Test Name'},
        {'email': 'test@example.com', 'name': 'Test Name'},
        {'email': 'test@example.com', 'password': 'password123'},
    ])
    def test_create_user_missing_field(self, payload):
        """Создание пользователя без обязательного поля"""
        response = requests.post(urls.Endpoints.register, json=payload)  # используем register
        
        assert response.status_code in [400, 403]
        assert response.json()['success'] is False