import logging, time
import FEM.petclinic.pages.home_page

from playwright.sync_api import Page

now = time.time()
logger = logging.getLogger(__name__)


def test_error(page: Page) -> None:
    logger.info("Go to 'Error-Page' button and generate an error/exception")
    FEM.petclinic.pages.home_page.go_to_error(page)

    logger.debug("Start check if error was successfully initiated.")
    assert page.get_by_text("Something happened...", exact=True)
    logger.info("Error / Exception in GUI was generated successfully")
