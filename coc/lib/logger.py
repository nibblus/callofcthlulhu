"""
    This file is part of tolyn.

    tolyn is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import logging
from typing import Union

LOGGER_NAME = "COC"
LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGER_LEVEL = logging.DEBUG

LOGGER = logging.getLogger(LOGGER_FORMAT)
LOGGER.setLevel(LOGGER_LEVEL)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
LOGGER.addHandler(stream_handler)

CRITICAL, ERROR, WARNING, INFO, DEBUG = 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'

LOG_LEVEL_NAMES = {CRITICAL: logging.CRITICAL,
                   ERROR: logging.ERROR,
                   WARNING: logging.WARNING,
                   INFO: logging.INFO,
                   DEBUG: logging.DEBUG}


def log_level_value(level: Union[int, str]) -> Union[int, str]:
    """
    Get the numeric log level
    :param level:
        If level is numeric, then check whether the value corresponds to a known log level.
        If level is string, then check if the level corresponds to a known log level name.
    Numeric value of the test level or the default version
    """
    if isinstance(level, int) and level in LOG_LEVEL_NAMES.values():
        return level
    elif isinstance(level, str) and level in LOG_LEVEL_NAMES.keys():
        return LOG_LEVEL_NAMES[level]
    raise ValueError(f"{level} is not an accepted value.")


def parse_log_level_name(level_name: str) -> int:
    """
    Translate loglevel name to log level value
    :param level_name: log level name to parse
    :return: correct log level value or debug in case of parsing errors
    """
    level = LOG_LEVEL_NAMES.get(level_name)
    if level is None:
        ValueError(f"{level_name} is not an accepted value.")
    return level


class LogExt:
    """
    Class to add log functions
    """

    def __init__(self, print_to_screen: bool = False):
        self.print_to_screen = print_to_screen
        self.logger = LOGGER  # logging.getLogger(self.logger_name())

    def logger_name(self):
        """
        By default, the logger for this class is identified by its class name.
        This method should be overloaded if instances want to share a loggers by returning a globally known name.
        :return: Class name
        """
        return self.__class__.__name__

    def _log_message(self, func, message="") -> None:
        """
        Log a message using the provided function.
        If the print_to_screen option is activated, the message will be printed as well
        :param func: logging function
        :param message: message to print
        """
        if self.print_to_screen:
            # print(message)
            pass
        func(message)

    def _log_messages(self, func, *messages, pre_blanks=0, post_blanks=0) -> None:
        """
        Log a message using the provided function.
        If the print_to_screen option is activated, the message will be printed as well
        :param func: logging function
        :param message: message to print
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        for i in range(pre_blanks):
            self._log_message(func)
        for message in messages:
            self._log_message(func, message)
            # func(message)
        for i in range(post_blanks):
            self._log_message(func)

    def debug(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log a debug message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self._log_messages(self.logger.debug, *messages, pre_blanks=pre_blanks, post_blanks=post_blanks)

    def info(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log an info message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self._log_messages(self.logger.info, *messages, pre_blanks=pre_blanks, post_blanks=post_blanks)

    def warning(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log a warning message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self._log_messages(self.logger.warning, *messages, pre_blanks=pre_blanks, post_blanks=post_blanks)

    def error(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log an error message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self._log_messages(self.logger.error, *messages, pre_blanks=pre_blanks, post_blanks=post_blanks)

    def critical(self, *messages, pre_blanks=0, post_blanks=0):
        """
        Log a critical message.
        :param messages: Message to log
        :param pre_blanks: number of blank lines to add before this log line
        :param post_blanks: number of blank lines to add after  this log line
        """
        self._log_messages(self.logger.critical, *messages, pre_blanks=pre_blanks, post_blanks=post_blanks)


if __name__ == '__main__':
    raise NotImplementedError(__file__)
