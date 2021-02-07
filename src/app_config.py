# Parse and handle the Config File
import yaml
import os
import logging

log = logging.getLogger(__name__)


class appconfig(object):
    """handle the configuration File"""

    def __init__(self):
        # Check if we actually have a config file available
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yml")):
            log.error("No configuration file found ...")
            # self._createdefault()
        self._parse()

        # Assign Config Values to Class
        # Global Settings
        self.debug = self.cfg.get('debug')
        self.local = self.cfg.get('use_local')
        self.pfd_creator = self.cfg.get('wkhtmltopdf_path')
        # DB settings
        self.db_path = self.cfg['database'].get('db_path')
        self.db_name = self.cfg['database'].get('database')
        self.db_user = self.cfg['database'].get('user')
        self.db_pwd = self.cfg['database'].get('password')
        self.db_ip = self.cfg['database'].get('address')
        self.db_port = self.cfg['database'].get('port')

        # Webserver Config
        self.web_port = self.cfg['webserver'].get('port')
        self.web_host = self.cfg['webserver'].get('host')
        # Path settings
        self.path = self.cfg['invoices'].get('basepath')

    def _parse(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yml"), "r") as ymlfile:
            # cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
            cfg = yaml.full_load(ymlfile)
        self.cfg = cfg

    def _createfolders(self):
        # Create all Folders we need for the tool
        pass

    def _createdefault(self):
        # Create a blank config file
        log.info("Creating default config file ...")

        config_file = {"debug": False, "use_local": True, 'wkhtmltopdf_path': "Please definde path for wkhtmltopdf.exe",
                       'database': {'address': '192.168.178.71', 'port': 3307, 'db_path': "",
                                    'database': "db_invoices", 'user': 'invoice_tool', 'password': ""},
                       'webserver': {'port': 8090, 'host': "0.0.0.0"},
                       'invoices': {'basepath': "C:\\Temp"}}

        with open(r'config.yml', 'w') as file:
            yaml.dump(config_file, file)


# Call the Configuration class
AppConfig = appconfig()
