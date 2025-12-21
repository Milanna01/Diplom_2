import pytest
import requests
from generators import generate_email, generate_password, generate_name
from urls import Endpoints
from data import TestUser


@pytest.fixture()
def new_user_data():
    """Данные нового пользователя"""
    return {
        'email': generate_email(),
        'password': generate_password(),
        'name': generate_name()
    }


@pytest.fixture()
def authenticated_user():
    """Авторизованный пользователь с автоматическим удалением"""
    user_data = {
        'email': generate_email(),
        'password': generate_password(),
        'name': generate_name()
    }
    
    # Регистрируем пользователя
    register_response = requests.post(Endpoints.register, json=user_data)
    assert register_response.status_code == 200
    
    # Получаем токен
    token = register_response.json()['accessToken']
    
    # Добавляем токен к данным пользователя
    user_data['token'] = token
    
    yield user_data
    
    # Удаляем пользователя после теста
    requests.delete(Endpoints.user_delete, headers={'Authorization': f'Bearer {token}'})


@pytest.fixture()
def existing_user():
    """Возвращает данные существующего тестового пользователя"""
    return {
        'email': TestUser.email,
        'password': TestUser.password,
        'name': TestUser.name
    }


@pytest.fixture(scope='session')
def available_ingredients():
    """Список ID ингредиентов"""
    response = requests.get(Endpoints.ingredients)
    assert response.status_code == 200
    return [ingredient['_id'] for ingredient in response.json()['data']]