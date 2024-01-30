import logging
import time
import FEM.petclinic.pages.login_page
from playwright.sync_api import Page, expect

now = time.time()
logger = logging.getLogger(__name__)
title = FEM.petclinic.properties.props.TITLE


def run_login(page: Page) -> None:
    logger.debug("Go to Login Page")
    FEM.petclinic.pages.login_page.LoginPage.go_to_login_page(page)

    logger.debug("Start title check on Login-Page.")
    logger.debug(f"Title: {page.title()}")
    if expect(page).to_have_title(str(title)):
        logger.debug("Title check on Login-Page completed")
    else:
        logger.debug("Title check on Login-Page failed")
