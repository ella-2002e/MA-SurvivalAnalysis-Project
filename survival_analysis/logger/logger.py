import logging

class CustomFormatter(logging.Formatter):
    
    """ 
        Custom formatter for Informative Logging
    """
    grey = "\x1b[38;20m"
    violet="\x1b[38;5;183m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - (%(message)s) - line: %(lineno)d"
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: violet + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }
    def format(self, record):
        """

        Parameters
        ----------
        record : takes the record
            

        Returns
        -------
        returns formated(colored) output
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


if __name__=='__main__':
    # Just en example
    import os 
    
    logger = logging.getLogger(os.path.basename(__file__))
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

    logger.debug("debug message")
    logger.info("Warning: Email has not been sent......")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")