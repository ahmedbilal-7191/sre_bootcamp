import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # DEBUG in dev, INFO in prod
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )