from playwright.sync_api import Page
import time, logging, re
import activeMq.properties
import activeMq.queues
from activeMq.properties import props

logger = logging.getLogger(__name__)

now = time.time()

url = activeMq.properties.props.url
stage = activeMq.properties.props.stage
title = activeMq.properties.props.title


def get_messages_retry_locator_list_in_current_queue(page: Page, dlq_name) -> list:
    logger.info(f"Trying to find message_id for existing dead message")
    message_retry_locator_list = []
    # message_ids_list = []
    table_locator = page.locator("//table[@id='messages']")
    table_locator.highlight()
    row_locator = table_locator.locator('tbody', has=page.locator('tr'))
    row_locator.highlight()
    time.sleep(1)
    row_locator_count = row_locator.count()
    if row_locator_count > 0:
        logger.info(f"There are messages to be handled, counted: {row_locator_count}")
        message_links_in_row = row_locator.get_by_role('link')
        message_links_in_row.highlight()
        time.sleep(1)

        for locator in message_links_in_row.all():
            locator.highlight()
            time.sleep(1)
            result = locator.get_attribute('href')

            target2check = 'message.jsp'
            if str(result).__contains__(target2check):
                # message_ids_list.append(locator.all_text_contents())
                logger.info(f"found message: {locator.all_text_contents()}")
                locator.click()
                row_locator_bci = page.locator('tr', has=page.locator('td'))
                row_locator_bci.highlight()
                time.sleep(1)
                target_td = row_locator_bci.get_by_text('Timestamp', exact=True)
                message_timestamp = target_td.locator('//../td[2]')
                logger.info(f"found associated timestamp: {message_timestamp.all_text_contents()}")
                target_td = row_locator_bci.get_by_text('breadcrumbId', exact=True)
                message_breadcrumbid = target_td.locator('//../td[2]')
                logger.info(f"found associated breadcrumbID: {message_breadcrumbid.all_text_contents()}")
                row_locator_cec = page.locator('tr', has=page.locator('td'))
                row_locator_cec.highlight()
                time.sleep(1)
                target_td = row_locator_cec.get_by_text('CamelExceptionCaught', exact=True)
                message_camel_exception_caught = target_td.locator('//../td[2]')
                logger.info(
                    f"found associated camel_exception_caught: {message_camel_exception_caught.all_text_contents()}")
                retry_opportunity = analyze_message_retry_opportunity(message_camel_exception_caught.all_text_contents())
                activeMq.queues.go2dead_letter_queue(page, dlq_name)

            target = 'moveMessage.action'
            if str(result).__contains__(target):
                if retry_opportunity:
                    logger.debug(f"adding message locator to retry list")
                    message_retry_locator_list.append(locator)

    message_counter = table_locator.count()
    logger.debug(f"message_id_locator_list: {message_retry_locator_list}")
    return message_retry_locator_list


def analyze_message_retry_opportunity(message_camel_exception_caught):
    logger.info(f"message analysis for retry opportunity started.")
    retry_opportunity = False
    exception_input = str(message_camel_exception_caught[0])
    pattern_list = props.pattern_list
    # pattern_list = [r"^.*(HTTP-401).*(Die Anmeldung ist fehlgeschlagen. Die Lizenzüberprüfung ist fehlgeschlagen).*$",
    #                 r"^.*(HTTP-401).*(Hash not valid for use in specified state).*$",
    #                 r"^.*(HTTP-401).*(Logon failed. Safe handle has been closed).*$",
    #                 r"^.*(HTTP-500).*(was deadlocked on lock resources with another process and has been chosen as the deadlock victim.).*$",
    #                 r"^.*(javax.ws.rs.ProcessingException: java.net.SocketTimeoutException: Read timed out).*$",
    #                 r"^.*(HTTP-500).*(Diese Aktion ist beim Status).*(nicht verf).*(Zeigen Sie das Fenster erneut an und versuchen Sie es noch einmal).*$"
    #                 ]
    for p in pattern_list:
        # pattern = re.compile(r"^.*(HTTP-500).*(Diese Aktion ist beim Status Erfasst nicht verf).*$", re.DOTALL)
        pattern = re.compile(fr"{p}", re.DOTALL)
        if pattern.match(exception_input):
            retry_opportunity = True
            logger.info(f"Let's retry processing the current message.")
    logger.info(f"message analysis finished.")
    return retry_opportunity


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
