import os
from configparser import ConfigParser

HOME = os.path.expanduser('~')
CONFIG_PATH = os.path.join(HOME, '.vault.ini')
config = ConfigParser()

if not os.path.isfile(CONFIG_PATH):
    STORAGE_PATH = os.path.join(HOME, '.vault')
    config['PATH'] = {
        'Password': os.path.join(STORAGE_PATH, 'app.key'),
        'Database': os.path.join(STORAGE_PATH, 'app.sqlite3')
    }

    os.makedirs(STORAGE_PATH, exist_ok=True)
    with open(CONFIG_PATH, 'w') as config_file:
        config.write(config_file)
else:
    config.read(CONFIG_PATH)
