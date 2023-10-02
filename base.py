import os
import git
import hashlib
import javalang


class Global(object):
    repo_cache_base_path = "/tmp/repo_cache"

    def __init__(self):
        self.os = os
        self.git = git
        self.hashlib = hashlib
        self.javalang = javalang

    def md5(self, string: str) -> str:
        return self.hashlib.md5(string.encode('utf-8')).hexdigest()