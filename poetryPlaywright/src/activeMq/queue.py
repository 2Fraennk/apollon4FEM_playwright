from playwright.sync_api import Page
import time, logging
import activeMq.properties

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

now = time.time()

url = activeMq.properties.props.url
stage = activeMq.properties.props.stage
title = activeMq.properties.props.title


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
                print("test4")
                logger.error(f"could not find the right dlq: searching for {page_title}")
                result = False
        else:
            pass
    return result



def list_messages_in_current_queue(page: Page, dlq_name) -> list:
    logger.info(f"Trying to find message_id for existing dead message")
    message_id_locator_list = []
    table_locator = page.locator("//table[@id='messages']")
    table_locator.highlight()
    row_locator = table_locator.locator('tbody', has=page.locator('tr'))
    row_locator.highlight()
    time.sleep(1)
    row_locator_count = row_locator.count()
    if row_locator_count > 0:
        logger.debug(f"There are messages to be deleted, counted: {row_locator_count}")
        message_links = row_locator.get_by_role('link')
        message_links.highlight()
        time.sleep(1)

        for i in message_links.all():
            result = i.get_attribute('href')
            # target = 'message.jsp'
            target = 'moveMessage.action'
            if str(result).__contains__(target):
                message_id_locator_list.append(i)

    message_counter = table_locator.count()
    logger.debug(f"message_id_locator_list: {message_id_locator_list}")
    return message_id_locator_list

def find_message_in_current_queue(page: Page, dlq_name, message_id) -> bool:
    logger.info(f"Trying to find message_id {message_id}")
    table_locator = page.locator("//table[@id='messages']")
    table_locator.highlight()
    row_locator = table_locator.locator('tr', has=page.locator('td', has_text=message_id))
    row_locator.highlight()
    row_locator_count = row_locator.count()
    logger.debug(f"Messages to be deleted counter: {row_locator_count}")

    # returned object must be unique to avoid multiple selections e.g. in case of a cropped message_id being found multiple times
    if row_locator_count == 1:
        result = True
    else:
        result = False

    return result


def run_retry_dl(page: Page, dlq_name, message_id) -> bool:
    logger.info("Retry the dead letter processing")
    result_find_message_in_current_queue = find_message_in_current_queue(page, dlq_name, message_id)

    page.once("dialog", lambda dialog: dialog.accept())

    # returned object must be unique to avoid multiple selections e.g. in case of a cropped message_id being found multiple times
    if result_find_message_in_current_queue:
        table_locator = page.locator("//table[@id='messages']")
        logger.debug(f"Found messages inside DLQ: {dlq_name}")
        row_locator = table_locator.locator('tr', has=page.locator('td', has_text=message_id))
        logger.debug(f"Found message: {message_id}")
        link_locator = row_locator.locator('//../td[9]/a[2]')
        if link_locator.count() == 1:
            logger.debug(f"Ensured message found is unique: {message_id}")
            link_locator.click()

            # check if message is gone after retry
            result_find_message_in_current_queue = find_message_in_current_queue(page, dlq_name, message_id)

            assert result_find_message_in_current_queue is False  # assert message has been deleted
            logger.info(f"Message {message_id} from queue {dlq_name} has been deleted")
            result = True
        else:
            logger.error("retry-link could not be found or is more than exactly 1")
            raise ValueError("retry-link could not be found or is more than exactly 1")
            result = False
    else:
        logger.debug("message_id could not be found or is more than exactly 1")
        result = False

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
