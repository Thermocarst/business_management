from settings import console_logger, writter_logger


def _test():
    console_logger.debug("Started debug")
    console_logger.info("Started info")
    console_logger.warning("Started warning")
    console_logger.error("Started error")
    writter_logger.warning("write some data")
    console_logger.debug("Finished debug")
    console_logger.info("Finished info")
    console_logger.warning("Finished warning")
    console_logger.error("Finished error")
    try:
        raise IndexError
    except IndexError as ex:
        console_logger.exception("error", exc_info=ex)


_test()