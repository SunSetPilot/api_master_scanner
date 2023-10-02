import os
import git

import config.settings
from modules.public_utils import md5


class GitManager(object):

    def __init__(self, repo_cache_base_path: str):
        self.repo_cache_base_path = repo_cache_base_path
        if not os.path.exists(self.repo_cache_base_path):
            os.makedirs(self.repo_cache_base_path)

    def get_repo(self, repo_url: str, branch: str) -> str:
        """
        Get a git repo from the cache or clone it if it doesn't exist
        :param repo_url: repo git url
        :param branch: repo branch
        :return: repo local path
        """
        repo_name_hash = md5(f"{repo_url}|{branch}")
        repo_path = os.path.join(self.repo_cache_base_path, repo_name_hash)
        if not os.path.exists(repo_path):
            try:
                git.Repo.clone_from(repo_url, repo_path, branch=branch)
            except Exception as e:
                raise Exception(f"Failed to clone repo {repo_url} to {repo_path}: {e}")
        return repo_path

    def delete_repo(self, repo_url: str, branch: str) -> None:
        """
        Delete a git repo from the cache
        :param repo_url: repo git url
        :param branch: repo branch
        """
        repo_name_hash = md5(f"{repo_url}|{branch}")
        repo_path = os.path.join(self.repo_cache_base_path, repo_name_hash)
        if os.path.exists(repo_path):
            try:
                os.system(f"rm -rf {repo_path}")
            except Exception as e:
                raise Exception(f"Failed to delete repo {repo_url} from {repo_path}: {e}")


git_manager = GitManager(repo_cache_base_path=config.settings.repo_cache_base_path)
