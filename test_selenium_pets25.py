import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from params import email, password, nickname


@pytest.fixture(autouse=True)
def testing(web_browser):
    web_browser = web_browser
    web_browser.get('http://petfriends.skillfactory.ru/login')

    yield
    web_browser.quit()


def test_show_my_pets(web_browser):
    web_browser.find_element(By.ID, "email").send_keys(email)
    web_browser.find_element(By.ID, "pass").send_keys(password)
    web_browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert web_browser.find_element(By.TAG_NAME, "h1").text == "PetFriends"

    web_browser.implicitly_wait(10)
    web_browser.find_element(By.LINK_TEXT, "Мои питомцы").click()
    assert web_browser.find_element(By.TAG_NAME, "h2").text == nickname

    images = web_browser.find_elements(By.CSS_SELECTOR, "div#all_my_pets>table>tbody>tr>th>img")
    names = web_browser.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr/td[1]")
    species = web_browser.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr/td[2]")
    ages = web_browser.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr/td[3]")

    nums = WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "html>body>div>div>div")))

    pets_with_photo = int(0)
    names_of_pets = []
    species_of_pets = []
    ages_of_pets = []

    # Проверяем, что присутствуют все питомцы.
    nums_of_pets = int(nums.text.split("\n")[1].split(":")[1].strip())
    assert nums_of_pets == len(names)

    for i in range(len(names)):
        assert images[i].get_attribute("src") != ""
        pets_with_photo += 1
        assert names[i].text != ""
        names_of_pets.append(names[i].text)
        assert species[i].text != ""
        species_of_pets.append(species[i].text)
        assert ages[i].text != ""
        ages_of_pets.append(ages[i].text)

    # Проверяем, что хотя бы у половины питомцев есть фото.
    assert nums_of_pets >= pets_with_photo / 2

    # Проверяем, что у всех питомцев есть имя, пол и возраст.
    assert nums_of_pets == len(names_of_pets)
    assert nums_of_pets == len(species_of_pets)
    assert nums_of_pets == len(ages_of_pets)

    # Проверяем, что у всех питомцев разные имена.
    assert len(names_of_pets) == len(set(names_of_pets))

    # Проверяем, что нет повторяющихся питомцев.
    assert len(names_of_pets) == len(set(names_of_pets)) and len(species_of_pets) == len(set(species_of_pets)) and \
           len(ages_of_pets) == len(set(ages_of_pets))
