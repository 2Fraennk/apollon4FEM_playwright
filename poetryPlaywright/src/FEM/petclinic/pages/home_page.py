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


def locate_element_find_owners(page: Page) -> Locator:
    """ Get locator for the page 'find owners' """
    element_find_owners = page.get_by_title("find owners", exact=True)
    element_find_owners.hightlight()
    time.sleep(1)
    if expect(element_find_owners):
        return element_find_owners
    else:
        logger.debug("ERROR : element_find_owners not found.")


def locate_element_error(page: Page) -> Locator:
    """ Get locator for the page 'Error' """
    element_error = page.get_by_text("Something happened...", exact=True)
    element_error.highlight()
    time.sleep(1)
    if expect(element_error):
        return element_error
    else:
        logger.debug("ERROR : element_error not found.")


def locate_element_veterinarians(page: Page) -> Locator:
    """ Get locator for the page 'Veterinarians' """
    element_veterinarians = page.get_by_role("link").get_by_text("Veterinarians", exact=True)
    element_veterinarians.highlight()
    time.sleep(1)
    if expect(element_veterinarians):
        return element_veterinarians
    else:
        logger.debug("ERROR : element_veterinarians not found.")


def go_to_find_owner(page: Page) -> Page:
    """ Got to the 'find owners' Page """
    element_find_owners = page.get_by_title("find owners", exact=True)
    element_find_owners.highlight()
    time.sleep(1)
    element_find_owners.click()
    time.sleep(1)
    return page


def go_to_error(page: Page) -> None:
    """ Generate an Error / Exception inside the GUI """
    element_error = page.get_by_title("trigger a RuntimeException to see how it is handled", exact=True)
    element_error.highlight()
    time.sleep(1)
    element_error.click()
    time.sleep(1)


def go_to_veterinarians(page: Page) -> None:
    """ Go to veterinarians page """
    element_veterinarians = locate_element_veterinarians(page)
    element_veterinarians.highlight()
    time.sleep(1)
    element_veterinarians.click()
    time.sleep(1)
