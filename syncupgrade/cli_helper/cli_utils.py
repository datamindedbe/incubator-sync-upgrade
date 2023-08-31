from os import environ
from shutil import rmtree
from typing import Union

from git import Repo
from typer import prompt

from syncupgrade.cli_helper.manage_registries import RegistryManager
from syncupgrade.exceptions.custom_exceptions import GitFolderNotFound
from syncupgrade.git_integration.git_wrapper import GitWrapper
from syncupgrade.git_integration.remote_git import RemoteGitContext
from syncupgrade.models.cli_models import InitOptions, ApplyCommandOptions
from syncupgrade.models.enum_models import ApplyMode
from syncupgrade.utils.parsing_utils import cli_console


class CliHelper:
    def __init__(self, cli_options: Union[InitOptions, ApplyCommandOptions]):
        self.cli_options = cli_options
        self.git_client = self.__get_git_client()
        self.registry_manager = RegistryManager(self.cli_options,
                                                self.git_client.get_root_path() if self.git_client else None)

    def dry_run(self):
        for refactoring_file_path, refactoring_object in self.registry_manager.get_codmods().items():
            refactoring_object.describe_changes(refactoring_file_path)

    def __apply_code_changes(self):
        for refactoring_file_path, refactoring_object in self.registry_manager.get_codmods().items():
            refactoring_object.apply_code_changes(refactoring_file_path)

    def apply_code(self):
        if not self.cli_options.activate_git:
            self.__apply_code_changes()
            return "Changes applied locally"

        if not self.git_client.check_current_branch(self.cli_options.new_branch_name):
            self.git_client.create_checkout_new_branch(self.cli_options.new_branch_name)
        self.__apply_code_changes()
        if self.cli_options.apply_mode != ApplyMode.pull_request:
            return f"Changes applied locally in branch {self.cli_options.new_branch_name}"
        if environ.get("GIT_TOKEN"):
            git_token = environ["GIT_TOKEN"]
        else:
            cli_console.log("You can set GIT_TOKEN environment variable to avoid prompt")
            git_token = prompt("Enter your git token", hide_input=True)
        return self.git_client.push_to_remote(self.cli_options, git_token)

    def process_registries(self):
        if self.cli_options.activate_git:
            self.git_client.create_checkout_new_branch(self.cli_options.new_branch_name)
        if self.cli_options.remote:
            return self.registry_manager.get_remote_registries(
                self.git_client.clone_remote_registries(self.cli_options.registry))
        return self.registry_manager.create_local_registries()

    def __get_git_client(self):
        try:
            return RemoteGitContext(GitWrapper().find_remote_provider())
        except GitFolderNotFound as found_no_git_repo:
            if self.cli_options.activate_git:
                raise GitFolderNotFound() from found_no_git_repo
            return self.__create_tempo_repo()

    @staticmethod
    def __create_tempo_repo():
        root_path = Repo.init().git_dir
        git_client = GitWrapper()
        rmtree(root_path)
        return git_client
