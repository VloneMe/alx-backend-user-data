#!/usr/bin/env python3
"""Demonstrates the use of regex to replace
occurrences of specific field values."""
import re
import logging
import mysql.connector
import os
from typing import List, Tuple


class RedactingFormatter(logging.Formatter):
    """A custom formatter to redact sensitive information from log messages."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter.

        Args:
            fields: A list of strings representing sensitive fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record with redacted sensitive information.

        Args:
            record: A LogRecord object containing log information.

        Returns:
            A string representing the formatted log message.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Establishes connection to the MySQL environment."""
    try:
        db_connect = mysql.connector.connect(
            user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
            host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            database=os.getenv('PERSONAL_DATA_DB_NAME')
        )
        return db_connect
    except mysql.connector.Error as e:
        logging.error("Error connecting to database: %s", e)
        raise


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Redacts sensitive information from log messages using regex.

    Args:
        fields: A list of strings representing sensitive fields to redact.
        redaction: A string representing the redacted value.
        message: A string representing the log message to be filtered.
        separator: A string representing
        the separator between field-value pairs.

    Returns:
        A string representing the filtered log message.
    """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    Returns a configured logging.Logger object.

    Returns:
        A logging.Logger object configured with a RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    target_handler = logging.StreamHandler()
    target_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    target_handler.setFormatter(formatter)

    logger.addHandler(target_handler)
    return logger


def fetch_users(cursor: mysql.connector.cursor.MySQLCursor) -> List[Tuple]:
    """
    Retrieves all users from the database.

    Args:
        cursor: A MySQLCursor object used to execute SQL queries.

    Returns:
        A list of tuples representing user records.
    """
    cursor.execute("SELECT * FROM users;")
    return cursor.fetchall()


def main() -> None:
    """
    Retrieves user data from the database and
    logs it with sensitive information redacted.
    """
    db = get_db()
    cursor = db.cursor()

    try:
        users = fetch_users(cursor)
        headers = [field[0] for field in cursor.description]
        logger = get_logger()

        for row in users:
            info_answer = ''
            for f, p in zip(row, headers):
                info_answer += f'{p}={(f)}; '
            logger.info(info_answer)

    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    main()
