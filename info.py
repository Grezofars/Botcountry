# Словарь с информацией о странах и их столицах
country_capital_dict = {
    "Россия": "Москва",
    "США": "Вашингтон",
    "Китай": "Пекин",
    "Австралия": "Канберра",
    "Австрия": "Вена",
    "Азербайджан": "Баку",
    "Албания": "Тирана",
    "Алжир": "Алжир"
    # Добавьте остальные страны и их столицы
}


# Функция для получения случайной страны и ее столицы
def get_random_country():
    import random
    country = random.choice(list(country_capital_dict.keys()))
    capital = country_capital_dict[country]
    return country, capital


# Словарь для хранения данных пользователей
user_data = {}


def get_user_data(user_id):
    return user_data[user_id]


def update_user_data(user_id, user_data):
    user_data[user_id] = user_data


# Функция для инициализации данных пользователя
def init_user_data(user_id):
    user_data[user_id] = {"score": 0, "current_question": None, "current_step": None}


# Функция для получения текущего вопроса для пользователя
def get_current_question(user_id):
    country, capital = get_random_country()
    user_data[user_id]["current_question"] = (country, capital)
    return f"Какая столица у страны {country}?"


# Функция для проверки ответа пользователя
def check_answer(user_id, answer):
    country, capital = user_data[user_id]["current_question"]
    if answer.lower() == capital.lower():
        user_data[user_id]["score"] += 1
        return True
    else:
        return False


# Функция для получения результатов пользователя
def get_user_score(user_id):
    score = user_data[user_id]["score"]
    return f"Твой результат: {score} из 10."
