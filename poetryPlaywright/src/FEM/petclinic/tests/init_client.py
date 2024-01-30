import time, logging
from playwright.sync_api import Playwright
import FEM.petclinic.properties

logger = logging.getLogger(__name__)

headless = FEM.petclinic.properties.props.HEADLESS
user = FEM.petclinic.properties.props.USER
password = FEM.petclinic.properties.props.PASSWORD


def browser_context(playwright: Playwright):
    """ Configure browser and run tests """
    browser = playwright.firefox.launch(headless=bool(headless))
    context = browser.new_context(
        http_credentials={
            "username": user,
            "password": password,
        }
    )
    return context


class Init:
    pass
