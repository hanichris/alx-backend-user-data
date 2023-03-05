#!/usr/bin/env python3
"""Obfuscate the log messages.

Regex is used to filter out log messages of certain field values.
"""
import re
from typing import List


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
