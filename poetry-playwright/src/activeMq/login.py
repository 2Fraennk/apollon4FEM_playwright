from playwright.sync_api import Page, expect
import os
import time

import activeMq.properties
from activeMq.properties import props

now = time.time()

stage = activeMq.properties.props.stage
title = activeMq.properties.props.title

# url = None
url = activeMq.properties.props.url
# if stage == "test":
#     url = f"https://esb-queue-test.mms-at-work.de:8162/admin"
# if stage == "prod":
#     url = f"https://esb-queue.mms-at-work.de:8162/admin"



def run_login(page: Page) -> None:
    """ Login """
    page.goto(url)
    # page.get_by_role("link", name=re.compile("ADFS")).click()
    page.wait_for_url(f"{url}/**")
    expect(page).to_have_title(str(title))


if url is None:
    print("PLEASE SET *_STAGE VARIABLE")
    exit(1)
