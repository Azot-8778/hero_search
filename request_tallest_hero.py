import requests


def get_height(hero):

    height_data = hero.get("appearance", {}).get("height", [])
    height_str = height_data[1]

    try:
        return int(height_str.replace("cm", "").strip())
    except ValueError:
        return 0

def get_tallest_hero_by_gender_and_work(gender: str, has_work: bool):
    url = "https://akabab.github.io/superhero-api/api/all.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Error receiving data from the API")

    heroes = response.json()

    filtered_heroes = []
    for hero in heroes:
        hero_gender = hero.get("appearance", {}).get("gender", "").lower()
        occupation = hero.get("work", {}).get("occupation", "").strip()
        occupation_exists = bool(occupation)

        if hero_gender == gender.lower() and occupation_exists == has_work:
            filtered_heroes.append(hero)

    if not filtered_heroes:
        return None

    tallest_hero = filtered_heroes[0]
    tallest_height = get_height(tallest_hero)

    for hero in filtered_heroes[1:]:
        current_height = get_height(hero)
        if current_height > tallest_height:
            tallest_hero = hero
            tallest_height = current_height

    return tallest_hero

if __name__ == "__main__":
    hero = get_tallest_hero_by_gender_and_work("Male", True)
    if hero:
        print(hero)
    else:
        print("Герой не найден по заданным критериям.")
