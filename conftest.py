import pytest
import requests
from helpers import generate_user_data
from urls import Endpoints
from data import TestUser


@pytest.fixture()
def new_user_data():
    """Данные нового пользователя"""
    return generate_user_data()


@pytest.fixture()
def authenticated_user():
    """Авторизованный пользователь с автоматическим удалением"""
    user_data = generate_user_data()
    
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