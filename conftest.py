import pytest
import uuid
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


@pytest.fixture
def web_browser(request):
    browser = driver
    browser.set_window_size(1400, 1000)

    yield browser

    if request.node.rep_call.failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            print('URL:', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass
