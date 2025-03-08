import logging
import logging.config


logger_setup = {
    "version": 1,

    "formatters": {
        "std_formatter": {"format": """[%(asctime)s.%(msecs)03d] - %(levelname)s - %(name)s | module: %(module)s | line №: %(lineno)s | function: %(funcName)s
msg: %(message)s
path: %(pathname)s""",
                          "datefmt": "%Y-%m-%d %H:%M:%S"},
        
        "file_formatter": {"format": "[%(asctime)s.(msecs)03d] %(levelname)s - %(name)s - " \
                           "module: %(module)s function: %(funcName)s line №: %(lineno)s msg: %(message)s",
                           },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "std_formatter"},
        
        "file": {"class": "logging.FileHandler",
                 "filename": "/tmp/journal.log",
                 "mode": "a",
                 "encoding": "utf-8",
                 "level": "WARNING",
                 "formatter": "file_formatter"},
    },
    "loggers": {"console": {"level": "DEBUG",
                            "handlers": ["console", ],
                            },                 
                
                "writter": {"level": "WARNING",
                            "handlers": ["file", ], },
                }
}


logging.config.dictConfig(logger_setup)


old_factory = logging.getLogRecordFactory()


class ColorizedOutput:

    """
    name: str
    msg: str
    levelname: str
    levelno: int
    pathname: str
    filename: str
    module: str
    exc_info: None
    exc_text: None
    stack_info: None
    lineno: int
    funcName: str
    """

    associations = {"DEBUG": "\033[32m", "INFO": "\033[36m", "WARNING": "\033[33m",
                    "ERROR": "\033[31m", "CANCEL": "\033[0m", "LINK": "\033[34m", 
                    "ERROR_BG": "\033[41m"}

    def __init__(self, rec_factory):
        self.rec_factory = rec_factory
        self.levelname = rec_factory.levelname
        self.color = self.levelname

    def set_output(self):
        self.rec_factory.msg = self.msg_template(self.rec_factory.msg)
        self.rec_factory.levelname = self.msg_template(self.levelname)
        self.rec_factory.pathname = self.msg_template(self.rec_factory.pathname, "LINK")

    def msg_template(self, msg, color=None):
        self.set_color(color)        
        return "%s%s%s" % (self.associations[self.color],
                           msg,
                           self.associations["CANCEL"])

    def set_color(self, color):
        if color:
            self.color = "ERROR_BG" if self.color == "ERROR" else color


def record_factory(*args, **kwargs):
    """
    https://docs.python.org/3/library/logging.html#logging.LogRecord
    """
    record = old_factory(*args, **kwargs)
    if record.name == "console":
        ColorizedOutput(record).set_output()
    return record


logging.setLogRecordFactory(record_factory)


console_logger = logging.getLogger("console")
writter_logger = logging.getLogger("writter")
