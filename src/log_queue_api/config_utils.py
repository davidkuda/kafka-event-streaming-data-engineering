from configparser import ConfigParser


def get_config():
    """Parses a config.ini file and returns the content as dictionary."""
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(open("config/kafka_config.ini", "r"))
    config = dict(config_parser["default"])
    return config


def get_consumer_config():
    config_parser = ConfigParser()
    config_parser.read_file(open("config/kafka_config.ini", "r"))
    config = dict(config_parser["default"])
    config.update(config_parser["consumer"])
    return config
