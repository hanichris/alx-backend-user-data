#!/usr/bin/env python3
"""Obfuscate the log messages.

Regex is used to filter out log messages of certain field values.
"""
import logging
import re
import sys
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns an obfuscated log message.

    Args:
        fields (List[str]): list of strings representing the fields
                            to obfuscate.
        redaction (str): string to obfuscate the given field with.
        message (str): string representing the log line.
        separator (str): string representing the character separating
                         all fields in the log line.
    Return:
        str: obfuscated log message.
    """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialization of variables.

        Args:
            fields (List[str]): list of strings representing the
                                fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incomming log records using `filter_datum`.

        Args:
            record (logging.LogRecord): contains all the info pertinent
                                        to the event being logged.
        Return:
            str: obfuscated log message.
        """
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a logger named `user_data` and logs upto `logging.INFO`.

    This logger doesn't propagate messages to other loggers and has
    a `StreamHandler` with `RedactingFormatter` as formatter. Uses
    `PII_FIELDS` to parameterize the formatter.
    """
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
