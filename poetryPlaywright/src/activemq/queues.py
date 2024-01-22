from playwright.sync_api import Page
import time, logging
import activemq.properties

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

now = time.time()

url = activemq.properties.props.url
stage = activemq.properties.props.stage
title = activemq.properties.props.title


def run_go2deadletter(page: Page, dlq_name, message_id) -> bool:
    logger.info(f"Go to message {message_id} inside dlq {dlq_name}")
    page.goto(f"{url}/queues.jsp")
    page.get_by_role("link", name=dlq_name, exact=True).click()
    page.get_by_role("link", name=message_id, exact=False).click()
    # time.sleep(5)
    title = page.title()

    if title.__contains__(message_id):
        result = True
    else:
        result = False
    return result


def go2dead_letter_queue(page: Page, dlq_name) -> bool:
    logger.info(f"Trying to find dlq {dlq_name}")
    page.goto(f"{url}/queues.jsp")
    links = page.get_by_role("link").filter(has_text='Browse')
    result = False
    for i in links.all():
        given_attribute = i.get_attribute('href')
        target_attribute = f"browse.jsp?JMSDestination={dlq_name}"
        if given_attribute == target_attribute:
            i.click()
            # check if we are really inside the right queue
            page_title = page.title().rsplit(':', 1)[1]
            logger.debug(f"page_title:: {page_title}")

            if dlq_name in page_title:
                logger.info(f"found the right dlq: title == {page_title}")
                result = True
                break
            else:
                logger.error(f"could not find the right dlq: searching for {page_title}")
                result = False
        else:
            pass
    return result

def find_existing_dead_letter_queues(page: Page) -> {}:
    logger.info("Trying to find current existing dead letter queues")
    page.goto(f"{url}/queues.jsp")
    dlqs = page.get_by_role("link", name="DLQ.", exact=False)
    dlqs_list_raw = dlqs.evaluate_all("list => list.map(element => element.textContent)")
    dlqs_list = []
    for i in dlqs_list_raw:
        i = i.strip()
        str_count = i.count("...")
        if str_count == 0:
            pass
        elif str_count == 1:
            i = str(i).rsplit('... ', 1)[1]
        dlqs_list.append(i)
    return dlqs_list
