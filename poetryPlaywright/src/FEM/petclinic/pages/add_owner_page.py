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


def locate_inputfield_first_name(page: Page) -> Locator:
    """ Get locator for the input field first name on page 'add owners' """
    logger.info("Start to find input field firstName.")
    inputfields = page.get_by_role("textbox")
    for i in inputfields.__getattribute__("id"):
        if i == "firstName":
            i.highlight()
            time.sleep(1)
            logger.info("Found input field firstName.")
            return i
        else:
            logger.exception("EXCEPTION : inputfield_first_name not found.")
            return None

def locate_button_find_owner(page: Page) -> Locator:
    """ Get locator for the button 'find owners' """
    button_find_owner = page.get_by_role("button").get_by_text("Find Owner", exact=True)
    button_find_owner.highlight()
    time.sleep(1)
    if expect(button_find_owner):
        return button_find_owner
    else:
        logger.error("ERROR : button_find_owner not found.")
        return None

def locate_button_add_owner(page: Page) -> Locator:
    """ Get locator for the button 'add owners' """
    button_add_owner = page.get_by_role("button").get_by_text("Add Owner", exact=True)
    button_add_owner.highlight()
    time.sleep(1)
    if expect(button_add_owner):
        return button_add_owner
    else:
        logger.error("ERROR : button_add_owner not found.")
        return None
