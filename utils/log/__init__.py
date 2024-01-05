import logging

logging.basicConfig(level=logging.WARN,
                    format='[[%(levelname)s]] %(asctime)s: %(pathname)s/%(filename)s:%(lineno)d - %(message)s')

logger = logging.getLogger()
