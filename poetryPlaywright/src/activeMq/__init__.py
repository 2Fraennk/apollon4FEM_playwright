# from .main import run

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG', filename='../logs/playwrightActiveMq.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
