# pytest -v --driver Chrome --driver-path \C:\Driver_for_Selenium\chromedriver.exe

import pytest
from settings import valid_email, valid_password, valid_login
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing_area():
    pytest.driver = webdriver.Chrome('C:\Driver_for_Selenium\chromedriver.exe')

    # Открываем стартовую страницу PetFriends:
    pytest.driver.get("https://petfriends.skillfactory.ru")

    yield
    pytest.driver.quit()

def testing_all_pets():
    # Неявное ожидание 5 секунд при каждом шаге
    pytest.driver.implicitly_wait(10)

    # Нажиманм на кнопку зарегистрироваться
    pytest.driver.find_element("xpath","//button[@onclick=\"document.location='/new_user';\"]").click()

    # Нажимаем на кнопку "У меня уже есть аккаунт"
    pytest.driver.find_element("link text","У меня уже есть аккаунт").click()

    # Вводим email
    pytest.driver.find_element("id","email").send_keys(valid_email)

    # Вводим пароль
    pytest.driver.find_element("id","pass").send_keys(valid_password)

    # Нажимаем на кнопку "Войти"
    pytest.driver.find_element("xpath","//button[@type='submit']").click()

    # Проверяем, что мы оказались на главной странице
    assert pytest.driver.find_element("tag name", 'h1').text == "PetFriends"

    if pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets':
       # Делаем скриншот главной страницы
       pytest.driver.save_screenshot('result_petfriends.png')
    else:
       raise Exception("login error")

    # Нажимаем кнопку меню "Мои питомцы"
    pytest.driver.find_element("xpath",'//*[@id="navbarNav"]/ul/li[1]/a').click()

    # Явное ожидание 10 сек.
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'all_my_pets')))

    # Проверяем, что мы оказались на странице со списком своих питомцев
    assert pytest.driver.find_element("tag name",'h2').text == valid_login

    # Объявляем четыре переменные, в которых записываем найденные элементы на странице:
    # в images — все картинки питомцев,
    # в names — все их имена,
    # в breeds — все породы,
    # в age — возраст питомцев

    images = pytest.driver.find_elements("xpath",'//*[@id="all_my_pets"]//img')
    names = pytest.driver.find_elements("xpath",'//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    breeds = pytest.driver.find_elements("xpath",'//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    age = pytest.driver.find_elements("xpath",'//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    # Находим количество своих питомцев, чтобы проверить, что присутствуют все питомцы
    names_of_pets = pytest.driver.find_elements("xpath", '//td[1]')
    unique_names_of_pets = len(names_of_pets)

    # Проверяем, что хотя бы у половины питомцев есть фото
    assert len(images) >= unique_names_of_pets/2

    names_text = []
    names_non_empty = []
    for i in range(unique_names_of_pets):
        names_text.append(names[i].text)
        # проверяем, если текстовое значение элемента не пустое, то добавляем его в список names_non_empty
        if names[i].text != '':
           names_non_empty.append(names[i].text)

    breeds_text = []
    breeds_non_empty = []
    breeds_text.append(breeds[i].text)
    # проверяем, если текстовое значение элемента не пустое, то добавляем его в список breeds_non_empty
    if breeds[i].text != '':
        breeds_non_empty.append(breeds[i].text)

    age_text = []
    age_non_empty = []
    for i in range(len(age)):
        age_text.append(age[i].text)
        # проверяем, если текстовое значение элемента не пустое, то добавляем его в список age_non_empty
        if breeds[i].text != '':
            age_text.append(age[i].text)

    # Проверяем, что у всех питомцев есть имя, возраст и порода
    assert unique_names_of_pets >= len(breeds_non_empty) and unique_names_of_pets >= len(names_non_empty) and \
           unique_names_of_pets >= len(age_non_empty)

    names_repeat = []
    # Проходимся по списку текстовых значений names_text и добавляем повторяющиеся его элементы в список names_repeat
    for n in range(unique_names_of_pets):
        for j in range(n+1,unique_names_of_pets):
            if names_text[n] == names_text[j]:
                names_repeat.append(names_text[n])

    # Проверяем, что у всех питомцев разные имена
    assert len(names_repeat) != 0

    pets = pytest.driver.find_elements("xpath",'//*[@id="all_my_pets"]/table/tbody/tr')

    pets_text = []
    pets_non_empty = []
    for i in range(unique_names_of_pets):
        pets_text.append(pets[i].text)

    # Проходим по списку pets_text и добавляем в список pets_non_empty повторяющиеся элементы
    for n in range(unique_names_of_pets):
        for j in range(n + 1, unique_names_of_pets):
            if pets_text[n] == pets_text[j]:
                pets_non_empty.append(pets_text[n])

    assert len(pets_non_empty) != 0