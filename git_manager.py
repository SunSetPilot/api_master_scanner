from base import Global


class GitManager(Global):

    def __init__(self):
        super(GitManager, self).__init__()
        if not self.os.path.exists(self.repo_cache_base_path):
            self.os.makedirs(self.repo_cache_base_path)

    def get_repo(self, repo_url: str, branch: str) -> str:
        """
        Get a git repo from the cache or clone it if it doesn't exist
        :param repo_url: repo git url
        :param branch: repo branch
        :return: repo local path
        """
        repo_name_hash = self.md5(f"{repo_url}|{branch}")
        repo_path = self.os.path.join(self.repo_cache_base_path, repo_name_hash)
        if not self.os.path.exists(repo_path):
            try:
                self.git.Repo.clone_from(repo_url, repo_path, branch=branch)
            except Exception as e:
                raise Exception(f"Failed to clone repo {repo_url} to {repo_path}: {e}")
        return repo_path

    def delete_repo(self, repo_url: str, branch: str) -> None:
        """
        Delete a git repo from the cache
        :param repo_url: repo git url
        :param branch: repo branch
        """
        repo_name_hash = self.md5(f"{repo_url}|{branch}")
        repo_path = self.os.path.join(self.repo_cache_base_path, repo_name_hash)
        if self.os.path.exists(repo_path):
            try:
                self.os.system(f"rm -rf {repo_path}")
            except Exception as e:
                raise Exception(f"Failed to delete repo {repo_url} from {repo_path}: {e}")


git_manager = GitManager()
