import os


class props():
    stage = os.getenv("ACTIVEMQ_STAGE")
    title = os.getenv("ACTIVEMQ_TITLE")

    if stage == "test":
        url = "https://testhost.domain:8162/admin"
    if stage == "prod":
        url = "https://prodhost.domain:8162/admin"

    def get_stage(self) -> str:
        return self.stage
