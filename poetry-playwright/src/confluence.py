from playwright.sync_api import Playwright, Page, sync_playwright, expect
import os
import re
import time

now = time.time()

stage = os.getenv("CONFLUENCE_STAGE")
user = os.getenv("CONFLUENCE_USER")
password = os.getenv("CONFLUENCE_PASSWORD")
domain = os.getenv("CONFLUENCE_DOMAIN")
title = os.getenv("CONFLUENCE_TITLE")
headless = False

url = None
if stage == "test" or stage == "stage":
    url = f"https://confluence-{stage}.{domain}"
if stage == "prod":
    url = f"https://confluence.{domain}"


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


def run_login(page: Page) -> None:
    """ Login """
    page.goto(url)
    # page.get_by_role("link", name=re.compile("ADFS")).click()
    page.wait_for_url(f"{url}/**")
    expect(page).to_have_title(re.compile(title))


def run_create_test_page(page: Page) -> None:
    """ Create simple page in personal space """
    page.goto(f"{url}/display/esb/Home")
    page.get_by_role("link", name="Create", exact=True).click()
    page.wait_for_url(f"{url}/pages/resumedraft.action**")
    page.get_by_placeholder("Page title").click()
    page.get_by_placeholder("Page title").fill(f"Playwright is awesome {now}")
    page.frame_locator("iframe[title=\"Rich Text Area\"]").get_by_label("Page content").click()
    page.frame_locator("iframe[title=\"Rich Text Area\"]").get_by_label("Page content").fill("test")
    page.get_by_role("button", name="Publish").click()
    time.sleep(2)
    expect(page).to_have_title(re.compile(f"Playwright is awesome {now}"))


def run_delete_test_page(page: Page) -> None:
    """ Delete created test page """
    page.goto(f"{url}/display/esb/playwright+is+awesome+{now}")
    page.get_by_role("link", name="More options").click()
    page.get_by_role("menuitem", name="Delete").click()
    page.locator("#delete-dialog-next").click()


if user is None or password is None:
    print()
    print("PLEASE SET CONFLUENCE_USER AND CONFLUENCE_PASSWORD VARIABLES")
    exit(1)
if url is None:
    print()
    print("PLEASE SET CONFLUENCE_STAGE VARIABLE")
    exit(1)

with sync_playwright() as playwright:
    run(playwright)
