class Endpoints:
    # Базовый URL API
    base_url = 'https://stellarburgers.education-services.ru'
    
    # Регистрация нового пользователя
    register = f'{base_url}/api/auth/register'
    # Авторизация пользователя
    login = f'{base_url}/api/auth/login'
    # Выход из системы
    logout = f'{base_url}/api/auth/logout'
    # Обновление токена
    refresh_token = f'{base_url}/api/auth/token'
    # Удаление пользователя
    user_delete = f'{base_url}/api/auth/user'
    # Создание заказа
    create_order = f'{base_url}/api/orders'
    # Получение заказов пользователя
    user_orders = f'{base_url}/api/orders'
    # Получение ингредиентов
    ingredients = f'{base_url}/api/ingredients'