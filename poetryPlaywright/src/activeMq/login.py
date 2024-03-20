from playwright.sync_api import Page, expect
import time
import activeMq.properties

now = time.time()

stage = activeMq.properties.Props.stage
title = activeMq.properties.Props.title
url = activeMq.properties.Props.url



def run_login(page: Page) -> None:
    """ Login """
    page.goto(url)
    # page.get_by_role("link", name=re.compile("ADFS")).click()
    page.wait_for_url(f"{url}/**")
    expect(page).to_have_title(str(title))


if url is None:
    print("PLEASE SET *_STAGE VARIABLE")
    exit(1)
