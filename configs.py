import os
import json
import re


class Config(object):

    _configs = None

    env = 'default'

    def __init__(self):
        env_file_path = "./.env"

        if os.path.isfile(env_file_path):
            with open(env_file_path) as envFile:
                self.env = envFile.readline().strip(' \t\n\r')

    def parsemycnf(self):
        home_path = os.getenv("HOME")
        options = {}

        mycnf_file_path = '%s/.my.cnf' % home_path

        with open(mycnf_file_path) as my_cnf:
            regex = r"[^\r\n]+"
            data_my_cnf = my_cnf.read()
            matches = re.findall(regex, data_my_cnf)

        for line in matches:
            kv = line.split('=')
            if len(kv) == 2:
                options[kv[0]] = kv[1]

        return options

    def _r_key_search(self, haystack, keys=None):
        if keys is None or len(keys) == 0:
            return haystack

        key = keys.pop(0)

        if key not in haystack:
            return None

        haystack = haystack[key]

        return self._r_key_search(haystack, keys)

    def get(self, key):
        self._configs = self.parse()

        keys = key.split('.')

        result = self._r_key_search(self._configs, keys)

        if result is None:
            raise KeyError()

        return result

    def parse(self):
        if Config._configs is not None:
            return self._configs

        with open('./config/%s.json' % self.env) as data_file:
            Config._configs = json.load(data_file)

        if "db" not in Config._configs:
            return Config._configs

        if "user" not in Config._configs["db"] or "password" not in Config._configs["db"]:
            db_options = self.parsemycnf()
            Config._configs["db"]["user"] = db_options["user"]
            Config._configs["db"]["password"] = db_options["password"]

        return Config._configs
