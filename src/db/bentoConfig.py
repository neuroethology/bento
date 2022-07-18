# bentoConfig.py

from getpass import getuser
from os.path import expanduser, exists, sep
from os import makedirs
import json
from cryptography.fernet import Fernet

class BentoConfig(object):
    """
    The BentoConfig class handles configuration data for Bento, particularly related to the experiments database.
    """

    def __init__(self):
        self.key = b'AKGnrrxYhjanPOEZIP1PIc_17YRCsO-fBmTuQyEeLX0='
        self.cipher_suite = Fernet(self.key)
        self._usePrivateDB = True
        self._username = getuser()
        self._password = ""
        self._host = ""
        self._port = "3307"
        self.bento_dir = expanduser("~") + sep + '.bento' + sep
        self.config_path = self.bento_dir + 'config.json'
        self._investigator_id = None

    def write(self):
        """
        Write the configuration data to the file "config.json" in the ".bento" subdirectory (folder) of
        the user's platform-specific home directory.

        :params: None
        :returns: None
        """
        print(f"BentoConfig.write: writing to path {self.config_path}")
        if not exists(self.config_path):
            makedirs(self.bento_dir, exist_ok=True)
        with open(self.config_path, 'w') as file:
            config = {
                'usePrivateDB': self._usePrivateDB,
                'username': self._username,
                'password': self._password,
                'host': self._host,
                'port': self._port,
                'investigator': self._investigator_id
            }
            json.dump(config, file)

    def read(self):
        """
        Read the configuration data from the file "config.json" in the ".bento" subdirectory (folder) of
        the user's platform-specific home directory.

        If the config file exists, the class instance is populated from its contents and the call returns True.
        If the config file doesn't exist, the call returns False

        :params: None
        :returns: True if the config file exists, otherwise False
        """
        if exists(self.config_path):
            with open(self.bento_dir + 'config.json') as file:
                config = json.load(file)
            self._usePrivateDB = config.get('usePrivateDB')
            self._username = config.get('username')
            self._password = config.get('password') # still encrypted
            self._host = config.get('host')
            self._port = config.get('port')
            self._investigator_id = config.get('investigator')
            return True
        else:
            return False

    def usePrivateDB(self):
        """
        Returns the value of the usePrivateDB config entry.
        :params: None
        :returns: value (bool)
        """
        return bool(self._usePrivateDB)

    def setUsePrivateDB(self, val):
        """
        Sets the flag specifying to use a private database on the user's machine.

        The private database file is named bento.db, and is placed in the .bento directory
        (folder) in the user's home directory.

        If this flag is set, username, password, host and port configuration values are ignored.

        Args:
            val (bool): Whether to use a private database or not.
        Returns:
            None
        """
        self._usePrivateDB = bool(val)

    def username(self):
        """
        Returns the previously set username.  This is used for access to a public database,
        specified by the "host" config item.

        Args:
            None
        Returns:
            str
        """
        return self._username

    def setUsername(self, username):
        """
        Sets the username to be used for access to a public database.

        Args:
            username (str): the username as established by the database administrator
        Returns:
            None
        """
        self._username = username

    def password(self):
        """
        Returns the password to be used for access to a public database.

        The password is decrypted from the form stored in the configuration file,
        and returned as plain text.

        Args:
            None
        Returns:
            str
        """
        try:
            return self.cipher_suite.decrypt(self._password.encode()).decode()
        except Exception:
            return ""

    def setPassword(self, password):
        """
        Sets the password to be used for access to a public database.

        The password is stored in the config file in an encrypted form.

        Args:
            password (str): the plain text password
        Returns:
            None
        """
        self._password = self.cipher_suite.encrypt(password.encode()).decode()

    def host(self):
        """
        Returns the hostname of a public database server used to store Bento experiments.

        The hostname should include domain names as needed to reach the server, e.g. mybentoserver.caltech.edu.

        Args:
            None
        Returns:
            str
        """
        return self._host

    def setHost(self, host):
        """
        Sets the hostname of the public database server used to storage and manage Bento experimental data.

        The hostname should include domain names as needed to reach the server, e.g. mybentoserver.caltech.edu.

        Args:
            host (str): the hostname of the server
        Returns:
            None
        """
        self._host = host

    def port(self):
        """
        Returns as a string the TCP/IP port number used to access the public database server.  For mySql or MariaDB servers,
        this should probably be 3307.

        Args:
            None
        Returns:
            str
        """
        return self._port

    def setPort(self, port):
        """
        Sets the TCP/IP port number used to access the public database server used to store Bento experimental data.

        For mySql or MariaDB, this should probably be 3307.

        Args:
            port (str): The port number, represented as a string.
        Returns:
            None
        """
        self._port = port

    def investigator_id(self):
        """
        Returns the id of the current investigator.

        This id needs to be a valid investigator id in the database, and is
        used widely by Bento when accessing data.

        Args:
            None
        Returns:
            int
        """
        return self._investigator_id

    def set_investigator_id(self, investigator_id):
        """
        Sets the investigator id to be used for a wide variety of database accesses,
        particularly sessions and trials.

        Args:
            investigator_id (int): the database id of the current investigator
        Returns:
            None
        """
        self._investigator_id = investigator_id