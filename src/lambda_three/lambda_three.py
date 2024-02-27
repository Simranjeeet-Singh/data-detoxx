import logging

def lambda_handler3(event, context):
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.INFO)
    logger.error('rcd10')
    raise RuntimeError