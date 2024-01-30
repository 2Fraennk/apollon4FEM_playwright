import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG', filename='../../logs/playwrightFEM.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')