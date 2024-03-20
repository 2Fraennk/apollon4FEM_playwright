from datetime import date

import jira

from properties import Props

import logging, sys

from jira import JIRA


class MyJira():
    logger = logging.getLogger(__name__)
    logging.basicConfig(level='INFO', filename='../../logs/jira.log', filemode='a',
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    date_today = date.today()

    logger.info("START : vars initialized. Let me do the work for you...")

    def init_jira_connection(self):
        jira = JIRA(server=Props.JIRA_URL,
                    token_auth=Props.JIRA_LOGIN_TOKEN,
                    )
        return jira

    def get_current_dlq_ticket(self, jiraclient):
        ticket = jiraclient.search_issues('project=ESB and summary~"jmx-activemq-dlq" and assignee = currentUser() and createdDate > startOfDay()', maxResults=1)
        if ticket != "":
            return ticket[0].key
            logger.info(f"Ticket {current_dlq_ticket} found")
        else:
            return 0
            logger.info(f"There is no Ticket.")

    def add_comments_to_ticket(self, jira, ticket, log_message):
        # parse log-message
        # log_message = 'this is a test message'
        comment = jira.add_comment(ticket, log_message)  # no Issue object required

    # def close_current_dql_ticket(self):
    # if all messages could be parse into ticket
    # jira.transition_issue(new_issue, 121)

    def get_current_dlq_ticket_status(self, current_dlq_ticket_key):
        current_dlq_ticket_status = jira.issue(current_dlq_ticket_key).get_field("status")
        return current_dlq_ticket_status

    def set_current_dlq_ticket_status(self, current_dlq_ticket_key, status):
        """
        status.name         | status.id
        Erfasst             | 121
        zurück zum Backlog  | 81
        In Arbeit           | 11
        zurück zu collected | 131
        Schließen           | 141
        """
        jira.transition_issue(current_dlq_ticket_key, status)


# client = MyJira()
# jira = client.init_jira_connection()
# current_dlq_ticket_key = client.get_current_dlq_ticket(jira)
# current_dlq_ticket_status = client.get_current_dlq_ticket_status(current_dlq_ticket_key)
# print(f"current_dlq_ticket_status: {current_dlq_ticket_status}")
# while client.get_current_dlq_ticket_status(current_dlq_ticket_key).name == "Erfasst":
    # print(current_dlq_ticket_status.name)
    # client.set_current_dlq_ticket_status(current_dlq_ticket_key, 11)
# client.add_comments_to_ticket(current_dlq_ticket_key)
# print(f"current_dlq_ticket_status: {current_dlq_ticket_status}")
