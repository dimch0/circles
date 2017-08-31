# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                      LOGGER                                                         #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import os
import datetime
import logging


class CirLogger(object):
    """ Logger class """
    def __init__(self):
        self.LOG_PATH = 'tmp/'
        self.CRITICAL = logging.CRITICAL
        self.ERROR = logging.ERROR
        self.WARNING = logging.WARNING
        self.INFO = logging.INFO
        self.DEBUG = logging.DEBUG
        self. LOG_NUMBER_KEEP_FILES = 1
        self.setup_logging(log_path=self.LOG_PATH)

    def setup_logging(self, log_path, file_name_addition=""):
        """ Setup the logging functionality

            :param log_path:            Path where the log file is going to be saved
            :type  log_path:            str
            :param file_name:           Requested log file name
            :type  file_name:           str
            :param file_name_addition:  (Optional) Additional information included in the log file name
            :type  file_name_addition:  str
            :return:                    log_file_name
            :rtype:                     str
        """

        log_file_name = '{0}.log'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        file_handler = logging.FileHandler("{0}/{1}".format(log_path, log_file_name))
        log_file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(log_file_formatter)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        log_console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_handler.setFormatter(log_console_formatter)
        console_handler.setLevel(logging.INFO)
        console_handler.setLevel(logging.DEBUG)
        logger = logging.getLogger()

        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return log_file_name

    def log(self, log_type, heading, details=""):
        """ Function to call the different logger functions.
            This logger functionality in the standard python logger function
            can print information to the console and/or a file, depending on the log type.

            :param log_type:  The type of logging, eg: Critical, Error, Warning, ....
            :type  log_type:  str
            :param heading:   Text to be logged
            :type  heading:   str
            :param details:   (Optional) The optional detailed information will be added
                                         by the heading information, separated by a ':'.
            :type  details:   str
            :return:          current time stamp
            :rtype:           datetime.datetime
        """
        now = datetime.datetime.now()
        logger = logging.getLogger()

        if details != "":
            details = ": %s" % details

        if log_type == self.CRITICAL:
            logger.info("%s%s" % (heading, details))
        elif log_type == self.ERROR:
            logger.error("%s%s" % (heading, details))
        elif log_type == self.WARNING:
            logger.warning("%s%s" % (heading, details))
        elif log_type == self.INFO:
            logger.info("%s%s" % (heading, details))
        elif log_type == self.DEBUG:
            logger.debug("%s%s" % (heading, details))
        else:
            logger.info("Unknown log-type (%s); %s%s" % (log_type, heading, details))
        return now
