# -*- coding: utf-8 -*-

import logging
import os
import sys
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from cleo import Command
from .helper import OutputHelper, StringHelper, DateHelper


class AbstractCommand(Command):
    def __init__(self, logger):
        super(AbstractCommand, self).__init__()
        self.logger = logger
        self.handler = None
        self._project_path = None

    def setup_logger(self, timestamp=False, name=None, max_bytes=1000000, backup_count=4):
        if not name:
            name = StringHelper.remove_suffix(StringHelper.snake_case(self.__class__.__name__), '_command')

        if timestamp:
            name = '{}-{}'.format(name, int(time.time()))

        filename = os.path.realpath(os.path.join(self._project_path, 'var', 'log', '{}.log'.format(name)))
        self.handler = RotatingFileHandler(
            filename=filename, maxBytes=max_bytes, backupCount=backup_count
        )
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
        sys.stdout.write('{}{}'.format(
            OutputHelper.colorize(
                'Logs are being writen to the file ',
                'yellow'
            ),
            OutputHelper.colorize(
                '"{}"\n\n'.format(filename),
                'cyan'
            )
        ))
        sys.stdout.flush()

    def get_date_option(self, key):
        input_date = self.option(key)
        if input_date and not DateHelper.is_valid_date(input_date):
            raise Exception('Invalid date format: {}, must be Y-m-d'.format(input_date))
        return datetime.strptime(input_date, '%Y-%m-%d').date() if input_date else None

    @property
    def project_path(self):
        return self._project_path

    @project_path.setter
    def project_path(self, project_path):
        self._project_path = project_path

    def validate_setup(self):
        if not self.handler:
            self.setup_logger(True)

    def info(self, message):
        self.validate_setup()
        self.logger.info(message)

    def success(self, message):
        self.validate_setup()
        self.logger.info(OutputHelper.colorize(message, 'green'))

    def comment(self, message):
        self.validate_setup()
        self.logger.info(OutputHelper.colorize(message, 'yellow'))

    def question(self, message):
        self.validate_setup()
        self.logger.info(OutputHelper.colorize(message, 'blue'))

    def error(self, message):
        self.validate_setup()
        self.logger.info(OutputHelper.colorize(message, 'red'))

    def line(self, message):
        pass
