from pathlib import Path
from shutil import rmtree

from git import Repo, InvalidGitRepositoryError, GitCommandError
from requests.models import Response

from syncupgrade.exceptions.custom_exceptions import GitFolderNotFound, CloneRemoteRegistryFailed, RestCallFailed
from syncupgrade.models.cli_models import ApplyCommandOptions


class GitWrapper:
    def __init__(self):
        try:
            self.repo = Repo(search_parent_directories=True)
        except InvalidGitRepositoryError as git_error:
            raise GitFolderNotFound() from git_error

    def create_checkout_new_branch(self, branch_name: str):
        if branch_name in self.__list_branches():
            raise ValueError(f"branch {branch_name} "
                             f"already exists, please delete the old branch first")
        refactor_branch = self.repo.create_head(branch_name)
        refactor_branch.checkout()

    def push_to_remote(self, cli_options: ApplyCommandOptions, git_token: str):
        self.__push(cli_options)
        base_branch = cli_options.base_branch if cli_options.base_branch else self.get_default_branch(git_token)
        return self.create_pull_request(git_token, branch_name=cli_options.new_branch_name,
                                        base_branch=base_branch, cli_options=cli_options)

    def __push(self, cli_options: ApplyCommandOptions):
        self.repo.git.add(all=True)
        self.repo.git.commit(m=f"upgrading {cli_options.package} to {cli_options.version}")
        self.repo.git.push('--set-upstream', 'origin',
                           self._find_branch_object(cli_options.new_branch_name))

    def check_current_branch(self, branch_name: str):
        return self.repo.active_branch.name == branch_name

    def create_pull_request(self, git_token: str, **kwargs):
        raise NotImplementedError("Git clients must implement this method")

    def get_default_branch(self, git_token: str):
        raise NotImplementedError("Git clients must implement this method")

    def format_rest_url(self):
        raise NotImplementedError("Git clients must implement this method")

    def _find_branch_object(self, branch_name: str):
        for branch in self.repo.heads:
            if branch.name == branch_name:
                return branch
        raise ValueError(f"{branch_name} not found locally")

    def __list_branches(self):
        return [
            branch.name for branch in self.repo.heads
        ]

    def clone_remote_registries(self, registry_link: str):
        try:
            remote_local_path = Path(self.repo.git_dir).parent.joinpath(registry_link.split("/")[-1][:-4])
            if remote_local_path.exists():
                rmtree(remote_local_path)
            self.repo.clone_from(registry_link, str(remote_local_path))
            return {"root_path": Path(self.repo.git_dir).parent, "remote_local_path": remote_local_path}
        except GitCommandError as clone_error:
            raise CloneRemoteRegistryFailed from clone_error

    def get_root_path(self):
        return self.repo.git_dir

    @staticmethod
    def process_rest_calls(response: Response):
        if response.ok:
            return response.json()
        raise RestCallFailed(response.reason, response.status_code)

    def find_remote_provider(self):
        for remote_provider in ("github", "gitlab", "bitbucket"):
            if remote_provider in self.repo.remotes.origin.url:
                return remote_provider
