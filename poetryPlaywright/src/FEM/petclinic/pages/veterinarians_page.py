import logging, time
from playwright.sync_api import Page, expect, Locator

import FEM.petclinic.properties

now = time.time()
url = FEM.petclinic.properties.props.URL
logger = logging.getLogger(__name__)


# class LoginPage:
def go_to_home_page(page: Page) -> None:
    """ Login """
    page.goto(url)


def locate_veterinarians(page: Page) -> Locator:
    """ Get rows from table of names on page 'Veterinarians' """
    logger.info("Start to find persons on page Veterinarians.")
    tbody = page.get_by_role("rowgroup")
    tbody.highlight()
    time.sleep(1)
    assert tbody
    logger.info("Found entries in table veterinarians.")
    return tbody
