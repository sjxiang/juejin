

import logging

_print_to_stderr = logging.StreamHandler()
_print_to_stderr.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)
_print_to_stderr.setLevel(logging.INFO)

logger = logging.getLogger("juejin")
logger.addHandler(_print_to_stderr)
logger.setLevel(logging.INFO)
logger.propagate = False

if __name__ == "__main__":
    logger.info("hello world")
    logger.error("hello world")
    logger.debug("hello world")  # 不打印
    logger.warning("hello world")
    logger.critical("hello world")