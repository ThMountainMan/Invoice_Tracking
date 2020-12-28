# Helper to interact with the Database

import yaml


def ParseConfig():
    with open("../recources/db_config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
    return cfg["database"]


def establish_connection():
    """ Establish a Database Connection """
    config = ParseConfig()

    print("Establishing Connection to :\n")
    print(f"Database : {config.get('address')}")
    print(f"User : {config.get('user')}")

    # TODO: Implement DB Connection


establish_connection()
