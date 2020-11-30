import os

import pytest

from .. import _migrate_uow_config, _create_config_dir, dirs, _check_apikey

TEST_KEY = "WyIyIiwiJDUkcm91bmRzPTUzNTAwMCRmYWtlX2RhdGEiLCJfZmFrZV9kYXRhXyJd.fake.fake"

LEGACY_CREDS = f"""
[api]
api_end_point = https://cchdo.ucsd.edu/api/v1
api_key = {TEST_KEY}
"""

def testCreateConfigDir(fs):
    _create_config_dir()

    assert os.path.exists(dirs.user_config_dir)

def testLegacyAuth(fs):
    CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "hdo_uow")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config")
    fs.create_file(CONFIG_FILE, contents=LEGACY_CREDS)

    assert _migrate_uow_config() is True

def testCheckAPIKey():
    assert _check_apikey(TEST_KEY)

    with pytest.raises(ValueError):
        _check_apikey("bad") 