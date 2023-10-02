from base import Global
from git_manager import git_manager


class ApiScanner(Global):
    def __init__(self):
        super(ApiScanner, self).__init__()
        self.git = git_manager
