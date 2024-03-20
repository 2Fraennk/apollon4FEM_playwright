from datetime import date
from properties import Props

import logging, sys

from jira import JIRA

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO', filename='../../logs/centraljira.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

jira = JIRA(server=Props.JIRA_URL,
            token_auth=Props.JIRA_LOGIN_TOKEN,
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
    'project': {'id': f"{Props.JIRA_PROJECT_ESB_ID}"},
    'summary': f"{date_today} - {service}",
    'description': f"Monitoring alert: {details}",
    'issuetype': {'name': 'ToDo'},
}

logger.info("START : Let me do the work for you...")

# issue_key = "ESB-2711"
# new_issue = jira.issue(issue_key)


new_issue = jira.create_issue(fields=issue_dict)
logger.info(f"Ticket {new_issue} created")

new_issue.update(assignee={'name': jira.current_user()})
logger.info(f"Updated {new_issue}: assigned to  YOU")

new_issue.update(priority={"id": "1"})
logger.info('Updated priority')

new_issue.update(fields={"labels": labels})
logger.info('Set labels')

# logger.info(new_issue.get_field("status"))
# new_issue.update(status={"id": "10031"})
jira.transition_issue(new_issue, 121)
logger.info(f"Ticket {new_issue.key} set to planing state")
# [(t['id'], t['name']) for t in transitions]
# logger.info(new_issue.get_field("status"))

# new_issue.update(resolution={"id": "1"})

logger.info(f"END : Ticket {new_issue} update finished")
