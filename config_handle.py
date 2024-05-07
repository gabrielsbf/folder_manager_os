import datetime as dt
import os
from configparser import ConfigParser

def first_exec(config: ConfigParser):
    cur_dir = os.getcwd()
    if config.has_section("PATHS"):
        return 0
    config.add_section("PATHS")
    patthern_path = input("Escreva o caminho da pasta de clientes: ")
    config.set("PATHS", "PATTERN_PATH", patthern_path.replace("\\", "/"))
    config.set("PATHS", "PROJECT_PATH", os.getcwd().replace("\\", "/"))
    
    with open(cur_dir + "/config.ini", "w") as file:
        config.write(file)

    