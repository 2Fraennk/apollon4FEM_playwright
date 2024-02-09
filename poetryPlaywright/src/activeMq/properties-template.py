
class props():
    stage = "Test"
    title = f"Esb.Broker-1.{stage} : ActiveMQ Console"
    ACTIVEMQ_DOMAIN = ""
    ACTIVEMQ_USER_TEST = ""
    ACTIVEMQ_PASSWORD_TEST = ""
    ACTIVEMQ_USER_PROD = ""
    ACTIVEMQ_PASSWORD_PROD = ""
    HEADLESS = False
    pattern_list = [r"^.*(HTTP-401).*.*$",
                    r"^.*(HTTP-500).*(deadlocked).*$",
                    ]

    if stage == "Test":
        url = "https://"
        ACTIVEMQ_USER = ACTIVEMQ_USER_TEST
        ACTIVEMQ_PASSWORD = ACTIVEMQ_PASSWORD_TEST
    if stage == "Prod":
        url = "https://"
        ACTIVEMQ_USER = ACTIVEMQ_USER_PROD
        ACTIVEMQ_PASSWORD = ACTIVEMQ_PASSWORD_PROD
