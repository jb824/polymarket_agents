import logging
import os

logging.basicConfig(
    level=logging.WARN,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create a logger for each child directory
loggers = {}
for dirpath, dirnames, filenames in os.walk('.'):
    log_level = 'INFO'  # Default log level
    if 'child' in dirnames:
        log_level = 'DEBUG'
    elif 'module' in dirnames:
        log_level = 'WARNING'

    logger_name = f'{dirpath.split("/")[-1]}.' + logging.getLogger().name
    loggers[logger_name] = logging.getLogger(logger_name)
    loggers[logger_name].setLevel(logging.getLevelName(log_level))
