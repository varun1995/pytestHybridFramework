import pytest
from selenium import webdriver
import os
from datetime import datetime

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FfService
from selenium.webdriver.firefox.options import Options as Ffoptions

from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


@pytest.fixture()
def setup(browser):
    if browser == 'edge':
        edge_options = EdgeOptions()
        print("Launching Edge browser.........")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
    elif browser == 'firefox':
        firefox_options = Ffoptions()
        print("Launching firefox browser.........")
        service = FfService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
    else:
        chrome_options = ChromeOptions()
        # You can add more options here if needed, for example:
        # chrome_options.add_argument('--headless')
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def pytest_addoption(parser):  # This will get the value from CLI /hooks
    parser.addoption("--browser")


@pytest.fixture()
def browser(request):  # This will return the Browser value to setup method
    return request.config.getoption("--browser")


########### pytest HTML Report ################

# It is hook for Adding Environment info to HTML Report
def pytest_configure(config):
    config._metadata['Project Name'] = 'Opencart'
    config._metadata['Module Name'] = 'CustRegistration'
    config._metadata['Tester'] = 'Pavan'


# It is hook for delete/Modify Environment info to HTML Report
@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)


#Specifying report folder location and save report with timestamp
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.htmlpath = os.path.abspath(os.curdir) + "\\reports\\" + datetime.now().strftime(
        "%d-%m-%Y %H-%M-%S") + ".html"
