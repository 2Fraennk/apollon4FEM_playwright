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


def run_login(page: Page) -> None:
    """ Login """
    page.goto(url)
    # page.get_by_role("link", name=re.compile("ADFS")).click()
    page.wait_for_url(f"{url}/**")
    expect(page).to_have_title(re.compile(title))


if url is None:
    print()
    print("PLEASE SET CONFLUENCE_STAGE VARIABLE")
    exit(1)
