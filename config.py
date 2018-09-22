#Not really used for much, however, is important for __init__.py

import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "yes"
