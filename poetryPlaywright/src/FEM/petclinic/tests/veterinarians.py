import logging, time
from playwright.sync_api import Page

import FEM.petclinic.pages.home_page
import FEM.petclinic.pages.veterinarians_page

now = time.time()
logger = logging.getLogger(__name__)
title = FEM.petclinic.properties.props.TITLE


def test_veterinarians(page: Page) -> None:
    """ Testsuite for testing functions on the veterinarians page """

    logger.info("Start to find veterinarians page")
    FEM.petclinic.pages.home_page.go_to_veterinarians(page)

    # logger.debug("Start title check on find veterinarians-page.")
    # headline_visible = page.get_by_role("heading", name="Veterinarians", exact=True).is_visible()
    # logger.debug(f"Found correct headline on page Find Owners: {headline_visible}")
    # assert headline_visible
    # logger.info("Headline check on veterinarians-page completed")

    logger.info("Search for Vetenarians")
    tbody = FEM.petclinic.pages.veterinarians_page.locate_veterinarians(page)
    number_rows = tbody.get_by_role("row").count()
    assert number_rows == 6
    logger.info("Found pre defined veterinarians on page Veterinarians.")
