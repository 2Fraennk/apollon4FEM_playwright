import logging, time
from playwright.sync_api import Page

import FEM.petclinic.pages.home_page

now = time.time()
logger = logging.getLogger(__name__)
title = FEM.petclinic.properties.props.TITLE


def test_home(page: Page) -> None:
    logger.info("Go to Home Page")
    FEM.petclinic.pages.home_page.go_to_home_page(page)

    logger.debug("Start title check on Home-Page.")
    logger.debug(f"Page title is: {page.title()}")
    assert page.title() == str(title)
    logger.info("Title check on Home-Page completed")
