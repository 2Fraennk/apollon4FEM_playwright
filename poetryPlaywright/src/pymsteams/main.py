from datetime import date

import logging, sys, pymsteams

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO', filename='../../logs/pymsteams.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>")

date_today = date.today()
host = sys.argv[1]
service = sys.argv[2]
details = sys.argv[3]
labels = []
labels.append(sys.argv[4])

for arg in sys.argv:
    logger.debug(arg)

message = {
    'project': {'id': f"{props.JIRA_PROJECT_ESB_ID}"},
    'summary': f"{date_today} - {service}",
    'description': f"Monitoring alert: {details}",
    'issuetype': {'name': 'ToDo'},
}

myTeamsMessage.text(message)

logger.info("START : Let me do the work for you...")

myTeamsMessage.send()

logger.info(f"END : Sending message {message} finished")
