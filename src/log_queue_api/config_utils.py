from configparser import ConfigParser


def get_config():
    """Parses a config.ini file and returns the content as dictionary."""
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(open("config/kafka_config.ini", "r"))
    config = dict(config_parser["default"])
    return config


def parse_config_file(config_file: str = "config/kafka_config.ini") -> dict:
    config = ConfigParser()
    config.read_file(open(config_file))
    sections = config.sections()
    configs = {}
    for section in sections:
        for item in config[section].items():
            k = item[0].upper()
            v = item[1]
            configs.update({k: v})
    return configs
