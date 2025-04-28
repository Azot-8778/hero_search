import pytest
from unittest.mock import patch
from request_tallest_hero import get_tallest_hero_by_gender_and_work

mock_heroes = [
    {
        "name": "HeroMan",
        "appearance": {"gender": "Male", "height": ["6'2", "188 cm"]},
        "work": {"occupation": "Fighting crime"}
    },
    {
        "name": "HeroWoman",
        "appearance": {"gender": "Female", "height": ["5'8", "173 cm"]},
        "work": {"occupation": "Saving the world"}
    },
    {
        "name": "LazyMan",
        "appearance": {"gender": "Male", "height": ["6'5", "196 cm"]},
        "work": {"occupation": ""}
    },
    {
        "name": "UnknownHeight",
        "appearance": {"gender": "Male", "height": ["-", "-"]},
        "work": {"occupation": "Unknown"}
    }
]

@pytest.fixture
def mock_get():
    with patch('requests.get') as mock:
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = mock_heroes
        yield mock

# 1. Мужчина с работой
def test_male_with_work(mock_get):
    hero = get_tallest_hero_by_gender_and_work("Male", True)
    assert hero is not None
    assert hero['name'] == "HeroMan"

# 2. Женщина с работой
def test_female_with_work(mock_get):
    hero = get_tallest_hero_by_gender_and_work("Female", True)
    assert hero is not None
    assert hero['name'] == "HeroWoman"

# 3. Мужчина без работы
def test_male_without_work(mock_get):
    hero = get_tallest_hero_by_gender_and_work("Male", False)
    assert hero is not None
    assert hero['name'] == "LazyMan"

# 4. Женщина без работы (нет подходящих)
def test_female_without_work(mock_get):
    hero = get_tallest_hero_by_gender_and_work("Female", False)
    assert hero is None

# 5. Пол в другом регистре
def test_gender_case_insensitive(mock_get):
    hero = get_tallest_hero_by_gender_and_work("male", True)
    assert hero is not None
    assert hero['name'] == "HeroMan"

# 6. Ошибка API запроса
def test_api_error():
    with patch('requests.get') as mock:
        mock.return_value.status_code = 500
        with pytest.raises(Exception, match="Ошибка при получении данных с API"):
            get_tallest_hero_by_gender_and_work("Male", True)

# 7. Неверные/пустые данные о росте
def test_unknown_height_ignored(mock_get):
    hero = get_tallest_hero_by_gender_and_work("Male", True)
    assert hero['name'] != "UnknownHeight"