import os
from configparser import ConfigParser, NoSectionError
import logging

from requests.auth import AuthBase
from appdirs import AppDirs

try:
    import google.colab
    COLAB = True
except ImportError:
    COLAB = False

logger = logging.getLogger(__name__)

dirs = AppDirs("edu.ucsd.cchdo", "cchdo")

CONFIG_FILE = "config.cfg"

CCHDO_PREFIX = "https://cchdo.ucsd.edu"

def _create_config_dir():
    os.makedirs(dirs.user_config_dir, exist_ok=True)

def _check_apikey(apikey):
    """check to see if the api key "looks" ok

    It cannot validate without the secrets but the
    payload can be checked to see if it at least decodes
    """
    import json
    from base64 import b64decode

    payload, *_ = apikey.split(".")

    try:
        logger.debug("Base64 decoding api key: %s...", apikey[:10])
        decoded = b64decode(payload.encode("ASCII"))
    except Exception as ex:
        logger.error("api key was either not valid ASCII or valid base64")
        raise ValueError("API could not be decoded") from ex

    try:
        logger.debug("JSON decoding api key: %s...", decoded[:10])
        json.loads(decoded)
    except Exception as ex:
        logger.error("api key payload could not be decoded as valid JSON")
        raise ValueError("API key payload not valid") from ex
    
    return True

def _migrate_uow_config():
    # lifted directly from the uow code
    CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "hdo_uow")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config")

    logger.debug("Checking to see if legacy config needs to me migrated")

    if not os.path.isfile(CONFIG_FILE):
        # file does not exist, so nothing to do
        return

    logger.info("A legacy hdo_uow config was found, migrating to standardized location")
    config = ConfigParser()
    config.read(CONFIG_FILE)

    apikey = config.get('api', 'api_key')
    _check_apikey(apikey)

    _write_apikey(apikey)

    os.remove(CONFIG_FILE)

    try:
        logger.debug("Removing legacy config dir")
        os.rmdir(CONFIG_DIR)
    except OSError:
        logger.info("Legacy config dir had files other than the config file, leaving in place")

    return True

def _write_apikey(apikey):
    config = _load_config()

    if not config.has_section("cchdo.auth"):
        config.add_section("cchdo.auth")

    config.set("cchdo.auth", "api_key", apikey)

    _write_config(config)

def _load_config():
    cfg_path = os.path.join(dirs.user_config_dir, CONFIG_FILE)
    config = ConfigParser()
    config.read(cfg_path)
    return config

def _write_config(config):
    _create_config_dir()
    cfg_path = os.path.join(dirs.user_config_dir, CONFIG_FILE)
    logger.debug("Writing config to: %s", cfg_path)
    with open(cfg_path, "w") as f:
        config.write(f)

def get_apikey():
    """
    """
    _migrate_uow_config()

    try:
        return os.environ["CCHDO_AUTH_API_KEY"]
    except KeyError:
        pass

    try:
        return _load_config().get("cchdo.auth", "api_key")
    except NoSectionError:
        pass

    logger.warn("An API Key could not be loaded from any source, many (not all) CCHDO API calls will fail")
    return ""
    
class CCHDOAuth(AuthBase):
    def __init__(self, apikey=None):
        if apikey is None:
            apikey = get_apikey()
        self._apikey = apikey

    def __call__(self, r):
        if not r.url.startswith(CCHDO_PREFIX):
            return r

        r.headers["X-Authentication-Token"] = self._apikey
        return r
