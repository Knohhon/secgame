"""

import config

import pytest
from gym import Env

from env.envNetwork import EnvNetwork
from env.network import Network


class TestEnv:
    def test_attr(self):
        env = EnvNetwork()
        assert hasattr(env, '')
"""