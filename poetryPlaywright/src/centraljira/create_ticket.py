from datetime import date
from properties import props

import logging, sys

from jira import JIRA

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO', filename='../../logs/centraljira.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

jira = JIRA(server=props.JIRA_URL,
            token_auth=props.JIRA_LOGIN_TOKEN,
            )

date_today = date.today()
host = sys.argv[1]
service = sys.argv[2]
details = sys.argv[3]
labels = []
labels.append(sys.argv[4])

for arg in sys.argv:
    logger.debug(arg)

issue_dict = {
    'project': {'id': f"{props.JIRA_PROJECT_ESB_ID}"},
    'summary': f"{date_today} - {service}",
    'description': f"Monitoring alert: {details}",
    'issuetype': {'name': 'ToDo'},
}

logger.info("START : Let me do the work for you...")

new_issue = jira.create_issue(fields=issue_dict)
logger.info(f"Ticket {new_issue} created")

new_issue.update(assignee={'name': jira.current_user()})
logger.info(f"Updated {new_issue}: assigned to  YOU")

new_issue.update(priority={"id": "1"})
logger.info('Updated priority')

new_issue.update(fields={"labels": labels})
logger.info('Set lables')

# new_issue.update(resolution={"id": "1"})

logger.info(f"END : Ticket {new_issue} update finished")
