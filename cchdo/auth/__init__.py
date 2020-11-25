import os.path
from configparser import ConfigParser

from requests.auth import AuthBase
from appdirs import AppDirs

try:
    import google.colab
    COLAB = True
except ImportError:
    COLAB = False

dirs = AppDirs("edu.ucsd.cchdo", "cchdo")

CCHDO_PREFIX = "https://cchdo.ucsd.edu"

def _create_config_dir():
    os.makedirs(dirs.user_config_dir, exist_ok=True)

def _check_api_key(api_key):
    """check to see if the api key "looks" ok

    It cannot validate without the secrets but the
    payload can be checked to see if it at least decodes
    """
    import json
    from base64 import b64decode

    payload, *_ = api_key.split(".")

    try:
        decoded = b64decode(payload.encode("ASCII"))
    except Exception as ex:
        raise ValueError("API could not be decoded") from ex

    try:
        json.loads(decoded)
    except Exception as ex:
        raise ValueError("API key payload not valid") from ex
    
    return True

def _migrate_uow_config():
    # lifted directly from the uow code
    CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "hdo_uow")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config")

    if not os.path.isfile(CONFIG_FILE):
        # file does not exist, so nothing to do
        return

    config = ConfigParser()
    config.read(CONFIG_FILE)
    api_key = config.get('api', 'api_key')
    _check_api_key(api_key)

    _create_config_dir()

    return True


def get_api_key():
    """
    """
    pass

class CCHDOAuth(AuthBase):
    def __init__(self, apikey=None):
        self._apikey = apikey

    def __call__(self, r):
        if not r.url.startswith(CCHDO_PREFIX):
            return r

        r.headers["X-Authentication-Token"] = self._apikey
        return r
