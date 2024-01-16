from playwright.sync_api import Page, expect
import os
import re
import time

now = time.time()

stage = os.getenv("CONFLUENCE_STAGE")
title = os.getenv("CONFLUENCE_TITLE")
domain = os.getenv("CONFLUENCE_DOMAIN")

url = None
if stage == "test" or stage == "stage":
    url = f"https://confluence-{stage}.{domain}"
if stage == "prod":
    url = f"https://confluence.{domain}"


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
