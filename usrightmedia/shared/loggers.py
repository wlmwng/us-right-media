import os
import logging
import logging.config
import yaml
from pprint import pprint

# Output all logs to the "logs" directory.

# Within each script or notebook:
# from usrightmedia.shared.loggers import get_logger
# use 'get_logger(type=...)' to log interesting stuff from the current script or notebook.


def _configure_logging(filename="default"):
    """Setup loggers based on YAML config.

    Args:
        filename (str, opt): filename to output to in 'logs' directory

    Returns:
        None

    """

    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(dir_path, "logging_config.yml"), "r") as f:
        config = yaml.safe_load(f.read())

        # all loggers using the 'file' handler will output to the same filename
        config["handlers"]["file"]["filename"] = os.path.join(
            dir_path, "..", "logs", f"{filename}.log"
        )

        logging.config.dictConfig(config)


def get_logger(logger_type="main", filename="default"):
    """
    Args:
        logger_type (str): type of logger specified in YAML config.

    Returns:
        Logger instance
    """

    _configure_logging(filename=filename)
    return logging.getLogger(logger_type)


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(dir_path, "logging_config.yml"), "r") as f:
        config = yaml.safe_load(f.read())
        pprint(config)
