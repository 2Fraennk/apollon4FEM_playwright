import logging, time
from playwright.sync_api import Page

import FEM.petclinic.pages.home_page
import FEM.petclinic.pages.find_owners_page
import FEM.petclinic.pages.add_owner_page

now = time.time()
logger = logging.getLogger(__name__)
title = FEM.petclinic.properties.props.TITLE


def test_owners(page: Page) -> None:
    """ Testsuite for testing owner funtions """

    logger.info("Go to find owners Page")

    page = FEM.petclinic.pages.home_page.go_to_find_owner(page)
    logger.debug("Start title check on find owners-Page.")
    headline_visible = page.get_by_role("heading", name="Find Owners", exact=True).is_visible()
    logger.debug(f"Found correct headline on page Find Owners: {headline_visible}")
    assert headline_visible
    logger.info("Headline check on find-owners-Page completed")

    # logger.info("Add owner Smith")
    # page = FEM.petclinic.pages.find_owners_page.locate_button_add_owner(page).click
    # time.sleep(1)

    logger.info("Search for owner Davis")
    input_field = FEM.petclinic.pages.find_owners_page.locate_inputfield_find_owners_last_name(page)
    input_field.first.highlight()
    input_field.first.fill("Davis")
    time.sleep(1)
    find_button = FEM.petclinic.pages.find_owners_page.locate_button_find_owner(page)
    find_button.click()
    logger.debug("Start result check on find owners.")
    tbody = page.get_by_role("rowgroup")
    tbody.highlight()
    time.sleep(1)
    number_rows = tbody.get_by_role("row").count()
    assert number_rows == 3
    logger.info("Found pre existing owners on page Find Owners.")
