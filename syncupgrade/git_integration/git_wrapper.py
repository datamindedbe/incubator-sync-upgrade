from git import Repo, InvalidGitRepositoryError
from json import dumps
from requests import post, get

from syncupgrade.exceptions.custom_exceptions import GitFolderNotFound
from syncupgrade.models.cli_models import ApplyCommandOptions
from syncupgrade.utils.parsing_utils import format_pr_link


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

    def _find_branch_object(self, branch_name: str):
        for branch in self.repo.heads:
            if branch.name == branch_name:
                return branch
        raise ValueError(f"{branch_name} not found locally")

    def __list_branches(self):
        return [
            branch.name for branch in self.repo.heads
        ]


class GithubClient(GitWrapper):
    def __init__(self):
        super().__init__()
        self.github_rest_url = f"{self.repo.remotes.origin.url.split('.git')[0]}".replace("github.com",
                                                                                          "api.github.com/repos")

    def create_pull_request(self, git_token: str, **kwargs):
        if kwargs.get("cli_options").package:
            pr_title = f"upgrading {kwargs.get('cli_options').package} to {kwargs.get('cli_options').version}"
        else:
            pr_title = "upgrading project"
        response = post(
            f"{self.github_rest_url}/pulls",
            headers={
                "Authorization": f"token {git_token}",
                "Content-Type": "application/json"},
            data=dumps({
                "title": pr_title,
                "head": kwargs.get("branch_name"),
                "base": kwargs.get("base_branch")
            }))
        if response.ok:
            return format_pr_link(response.json().get("url"))
        return response.json()

    def get_default_branch(self, git_token: str):
        response = get(
            self.github_rest_url,
            headers={
                "Authorization": f"token {git_token}",
                "Content-Type": "application/json"},
        )
        if response.ok:
            return response.json().get("default_branch")
