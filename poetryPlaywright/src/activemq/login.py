from playwright.sync_api import Page, expect
import time

import activemq.properties

now = time.time()

stage = activemq.properties.props.stage
title = activemq.properties.props.title
url = activemq.properties.props.url



def run_login(page: Page) -> None:
    """ Login """
    page.goto(url)
    # page.get_by_role("link", name=re.compile("ADFS")).click()
    page.wait_for_url(f"{url}/**")
    expect(page).to_have_title(str(title))


if url is None:
    print("PLEASE SET *_STAGE VARIABLE")
    exit(1)
