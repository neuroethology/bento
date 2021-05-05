# bentoConfig.py

from getpass import getuser
from os.path import expanduser, exists, sep
from os import makedirs
import json
from cryptography.fernet import Fernet

class BentoConfig(object):

    def __init__(self):
        self.key = b'AKGnrrxYhjanPOEZIP1PIc_17YRCsO-fBmTuQyEeLX0='
        self.cipher_suite = Fernet(self.key)
        self._username = getuser()
        self._password = ""
        self._host = ""
        self._port = "3307"
        self.bento_dir = expanduser("~") + sep + '.bento' + sep
        self.config_path = self.bento_dir + 'config.json'
        self._investigator_id = None

    def write(self):
        if not exists(self.config_path):
            makedirs(self.bento_dir, exist_ok=True)
        with open(self.config_path, 'w') as file:
            config = {
                'username': self._username,
                'password': self._password,
                'host': self._host,
                'port': self._port,
                'investigator': self._investigator_id
            }
            json.dump(config, file)

    def read(self):
        if exists(self.config_path):
            with open(self.bento_dir + 'config.json') as file:
                config = json.load(file)
            self._username = config.get('username')
            self._password = config.get('password') # still encrypted
            self._host = config.get('host')
            self._port = config.get('port')
            self._investigator_id = config.get('investigator')
            return True
        else:
            return False

    def username(self):
        return self._username

    def setUsername(self, username):
        self._username = username

    def password(self):
        try:
            return self.cipher_suite.decrypt(self._password.encode()).decode()
        except Exception:
            return ""
        
    def setPassword(self, password):
        self._password = self.cipher_suite.encrypt(password.encode()).decode()

    def host(self):
        return self._host

    def setHost(self, host):
        self._host = host

    def port(self):
        return self._port

    def setPort(self, port):
        self._port = port

    def investigator_id(self):
        return self._investigator_id

    def set_investigator_id(self, investigator_id):
        self._investigator_id = investigator_id