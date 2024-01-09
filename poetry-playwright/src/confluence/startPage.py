from playwright.sync_api import Playwright, sync_playwright
import os

from confluence.login import run_login
from confluence.testPage import run_create_test_page, run_delete_test_page

# now = time.time()

stage = os.getenv("CONFLUENCE_STAGE")
user = os.getenv("CONFLUENCE_USER")
password = os.getenv("CONFLUENCE_PASSWORD")
# domain = os.getenv("CONFLUENCE_DOMAIN")
# title = os.getenv("CONFLUENCE_TITLE")
headless = False




def run(playwright: Playwright) -> None:
    """ Configure browser and run tests """
    browser = playwright.firefox.launch(headless=headless)
    context = browser.new_context(
        http_credentials={
            "username": user,
            "password": password,
        }
    )

    page = context.new_page()

    try:
        run_login(page)
        run_create_test_page(page)
        run_delete_test_page(page)
    finally:
        context.close()
        browser.close()


if user is None or password is None:
    print()
    print("PLEASE SET CONFLUENCE_USER AND CONFLUENCE_PASSWORD VARIABLES")
    exit(1)


with sync_playwright() as playwright:
    run(playwright)
