from json import dumps
from re import search
from urllib.parse import quote

from requests import post, get

from syncupgrade.git_integration.git_wrapper import GitWrapper
from syncupgrade.utils.parsing_utils import format_github_pr_link


class GithubClient(GitWrapper):
    def __init__(self):
        super().__init__()
        self.github_rest_url = self.format_rest_url()

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
        if result := self.process_rest_calls(response):
            return format_github_pr_link(result.get("url"))

    def get_default_branch(self, git_token: str):
        response = get(
            self.github_rest_url,
            headers={
                "Authorization": f"token {git_token}",
                "Content-Type": "application/json"},
        )
        if result := self.process_rest_calls(response):
            return result.get("default_branch")

    def format_rest_url(self):
        return f"{self.repo.remotes.origin.url.split('.git')[0]}".replace("github.com", "api.github.com/repos")


class GitlabClient(GitWrapper):
    def __init__(self):
        super().__init__()
        self.gitlab_rest_url = self.format_rest_url()

    def format_rest_url(self):
        return f"https://gitlab.com/api/" \
               f"v4/projects/{quote(self.repo.remotes.origin.url.split(':')[-1].replace('.git', ''), safe='')}"

    def create_pull_request(self, git_token: str, **kwargs):
        if kwargs.get("cli_options").package:
            pr_title = f"upgrading {kwargs.get('cli_options').package} to {kwargs.get('cli_options').version}"
        else:
            pr_title = "upgrading project"
        response = post(
            f"{self.gitlab_rest_url}/merge_requests",
            headers={
                "Authorization": "Bearer {0}".format(git_token),
                "Content-Type": "application/json"},
            data=dumps({
                "title": pr_title,
                "source_branch": kwargs.get("branch_name"),
                "target_branch": kwargs.get("base_branch")
            }))
        if result := self.process_rest_calls(response):
            return f"PR link {result.get('web_url')}"

    def get_default_branch(self, git_token: str):
        response = get(
            f"{self.gitlab_rest_url}",
            headers={
                "Authorization": "Bearer {0}".format(git_token),
                "Content-Type": "application/json"},
        )
        if result := self.process_rest_calls(response):
            return result["default_branch"]


class BitbucketClient(GitWrapper):
    def __init__(self):
        super().__init__()
        self.bitbucket_rest_url = self.format_rest_url()

    def format_rest_url(self):
        repo_path = search(r'(?<=\.org)(.*)(?=\.git)', self.repo.remotes.origin.url).group(1).strip("/")
        domain_path = search(r'@([^/]+\.org)', self.repo.remotes.origin.url).group(1)
        return f"https://api.{domain_path}/2.0/repositories/{repo_path}"

    def get_default_branch(self, git_token: str):
        response = get(
            self.bitbucket_rest_url,
            headers={
                "Authorization": "Bearer {0}".format(git_token),
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        if result := self.process_rest_calls(response):
            return result["mainbranch"]["name"]

    def create_pull_request(self, git_token: str, **kwargs):
        if kwargs.get("cli_options").package:
            pr_title = f"upgrading {kwargs.get('cli_options').package} to {kwargs.get('cli_options').version}"
        else:
            pr_title = "upgrading project"
        response = post(
            f"{self.bitbucket_rest_url}/pullrequests",
            headers={
                "Authorization": "Bearer {0}".format(git_token),
                "Accept": "application/json",
                "Content-Type": "application/json"},
            data=dumps({
                "title": pr_title,
                "source": {
                    "branch": {
                        "name": kwargs.get("branch_name")
                    }
                },
                "destination": {
                    "branch": {
                        "name": kwargs.get("base_branch")
                    }
                }}))
        if result := self.process_rest_calls(response):
            return f"PR link {result['links']['html']['href']}"


class RemoteGitContext(GitWrapper):
    map_dict = {
        "github": GithubClient,
        "gitlab": GitlabClient,
        "bitbucket": BitbucketClient
    }

    def __init__(self, remote: str) -> None:
        super().__init__()
        self._remote = self.map_dict[remote]()

    def create_pull_request(self, git_token: str, **kwargs):
        return self._remote.create_pull_request(git_token, **kwargs)

    def get_default_branch(self, git_token: str):
        return self._remote.get_default_branch(git_token)

    def format_rest_url(self):
        return self._remote.format_rest_url()
