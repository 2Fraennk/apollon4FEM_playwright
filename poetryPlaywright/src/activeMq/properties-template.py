
class props():
    stage = "Test"
    title = f"Esb.Broker-1.{stage} : ActiveMQ Console"
    ACTIVEMQ_DOMAIN = ""
    ACTIVEMQ_USER_TEST = ""
    ACTIVEMQ_PASSWORD_TEST = ""
    ACTIVEMQ_USER_PROD = ""
    ACTIVEMQ_PASSWORD_PROD = ""
    HEADLESS = False
    search_pattern_list = [r"^.*(HTTP-401).*(Die Anmeldung ist fehlgeschlagen. Die Lizenzüberprüfung ist fehlgeschlagen).*$",
                           r"^.*(HTTP-401).*(Hash not valid for use in specified state).*$",
                           r"^.*(HTTP-401).*(Logon failed. Safe handle has been closed).*$",
                           r"^.*(HTTP-500).*(was deadlocked on lock resources with another process and has been chosen as the deadlock victim.).*$",
                           r"^.*(javax.ws.rs.ProcessingException: java.net.SocketTimeoutException: Read timed out).*$",
                           r"^.*(HTTP-500).*(Diese Aktion ist beim Status).*(nicht verf).*(Zeigen Sie das Fenster erneut an und versuchen Sie es noch einmal).*$"
                           ]

    if stage == "Test":
        url = "https://"
        ACTIVEMQ_USER = ACTIVEMQ_USER_TEST
        ACTIVEMQ_PASSWORD = ACTIVEMQ_PASSWORD_TEST
    if stage == "Prod":
        url = "https://"
        ACTIVEMQ_USER = ACTIVEMQ_USER_PROD
        ACTIVEMQ_PASSWORD = ACTIVEMQ_PASSWORD_PROD
