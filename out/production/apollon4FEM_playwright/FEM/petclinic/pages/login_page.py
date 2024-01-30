from playwright.sync_api import Page, expect
import time
import FEM.petclinic.properties

now = time.time()
url = FEM.petclinic.properties.props.URL


class LoginPage:
    def go_to_login_page(self: Page) -> None:
        """ Login """
        self.goto(url)
        self.wait_for_url(f"{url}/**")
