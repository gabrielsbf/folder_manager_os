from configparser import ConfigParser
from config_handle import *


dir_name = os.getcwd().split('\\')[-1]
if dir_name == 'dist':
    os.chdir("..")
config = ConfigParser()
config.read('config.ini')
first_exec(config)

PATTERN_PATH = config.get("PATHS", "pattern_path") + '/'
PROJECT_PATH = config.get("PATHS", "project_path") + '/'