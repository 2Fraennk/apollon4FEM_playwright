import time

from playwright.sync_api import sync_playwright
from FEM.petclinic.tests.init_client import *
from FEM.petclinic.tests.login import *
from FEM.petclinic.tests.error import *
from FEM.petclinic.tests.owners import *

logger = logging.getLogger(__name__)


def test_run(playwright: Playwright) -> None:
    """ Configure browser and run tests """
    context = FEM.petclinic.tests.init_client.browser_context(playwright)

    page = context.new_page()

    try:
        logger.debug(f"Start checking local installation of petclinic")

        test_home(page)

        for i in range(5):
            test_error(page)

        test_home(page)

        test_owners(page)

        test_home(page)

    except(RuntimeError, Exception):
        logger.error(f"Exception")
        raise Exception


with sync_playwright() as playwright:
    test_run(playwright)
