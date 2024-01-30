import time, os, logging
from playwright.sync_api import Playwright, sync_playwright

import FEM.petclinic.tests.init_client
from FEM.petclinic.properties import props
from FEM.petclinic.tests.init_client import *
from FEM.petclinic.tests.login import *

logger = logging.getLogger(__name__)


def run(playwright: Playwright) -> bool:
    """ Configure browser and run tests """
    context = FEM.petclinic.tests.init_client.browser_context(playwright)

    page = context.new_page()

    try:
        logger.debug(f"Start checking local installation of petclinic")

        run_login(page)
    except:
        pass


with sync_playwright() as playwright:
    run(playwright)
