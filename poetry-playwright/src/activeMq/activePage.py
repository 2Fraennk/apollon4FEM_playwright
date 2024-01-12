import time

from playwright.sync_api import Playwright, sync_playwright
import os
import logging

from activeMq.login import run_login
from activeMq.queue import go2dead_letter_queue, run_retry_dl, find_existing_dead_letter_queues, \
    list_messages_in_current_queue

logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

user = os.getenv("ACTIVEMQ_USER")
password = os.getenv("ACTIVEMQ_PASSWORD")
headless = False


def run(playwright: Playwright) -> bool:
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
        # dlq_name_input = run_input_dlq_name()
        # message_id = run_input_message_id()

        dlq_name_prefix = "DLQ."
        dlq_name = f"{dlq_name_prefix}MyService.ResponseController.AD.Group.Update"
        message_id = "all"  # "ID:q4deumsy0ca-34078-1702044626441-18:341:1:1:2"  #"all"  # "ID:q4deumsy0ca-34078-1702044626441-18:303:1:1:3"

        logger.info(f"{dlq_name}, {message_id}")

        run_login(page)

        if message_id == 'all':
            found_dead_letter_queues = find_existing_dead_letter_queues(page)
            if list(found_dead_letter_queues).__len__() > 0:
                logger.info("Found some DLQs")
                for i in found_dead_letter_queues:
                    print("i: ", i)
                    go2dead_letter_queue(page, i)
                    message_id_locator_list = list_messages_in_current_queue(page, i)
                    if message_id_locator_list.__len__() > 0:
                        logger.info(f"Found some messages in queue: {dlq_name}")
                        # message_id_locator_list.
                result = True
            else:
                logger.info("Could not find any DLQs")
                result = False
        elif message_id != "":
            logger.debug(f"message_id is set to: {message_id}")
            result_go2dead_letter_queue = go2dead_letter_queue(page, dlq_name)

            if result_go2dead_letter_queue:
                logger.debug(f"result_go2dead_letter_queue is set to: {result_go2dead_letter_queue}")
                result_run_retry_dl = run_retry_dl(page, dlq_name, message_id)
                logger.debug(f"result_run_retry_dl is set to: {result_run_retry_dl}")
                if result_run_retry_dl:
                    return True
                else:
                    return False
        else:
            logger.error("No message_id was given")
            result = False
    finally:
        context.close()
        browser.close()


if user is None or password is None:
    logger.error("PLEASE SET *_USER AND *_PASSWORD VARIABLES")
    raise ValueError("PLEASE SET *_USER AND *_PASSWORD VARIABLES")
    exit(1)

with sync_playwright() as playwright:
    run(playwright)
