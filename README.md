
![Build(3)](https://github.com/datamindedbe/sync-upgrade/assets/63344830/1c63825e-e988-4d2e-ab8c-5f99975e7d01)


SyncUpgrade is an automated Python refactoring tool that facilitates large-scale refactoring across diverse projects while
ensuring preservation of your code style and syntax. It offers a user-friendly API and a command-line interface (CLI) to
define specific code refactoring rules, resulting in the generation of refactored code.

[![Tests](https://github.com/datamindedbe/sync-upgrade/actions/workflows/Tests.yml/badge.svg?branch=main&event=push)](https://github.com/datamindedbe/sync-upgrade/actions/workflows/Tests.yml)

Using SyncUpgrade to upgrade a DAG from Airflow 1 to Aiflow 2 would look something like this

![demo](https://github.com/datamindedbe/sync-upgrade/assets/63344830/9a38030f-049a-4539-a272-19b0f445b15b)



# Installation

SyncUpgrade can be easily installed using most common Python packaging tools.
We recommend installing the latest stable release from PyPI with pip

```shell
pip install sync-upgrade
```

# Usage

```console
refactor init --help
                           
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --package                 TEXT  Package to upgrade                                                             │ 
│ --version                 TEXT  New package version                                                            │ 
│ --registry                TEXT  Directory where refactoring files are saved [default: ./refactoring_files/]    │ 
│ --git         --no-git          Activate git [default: git]                                                    │ 
│ --help                          Show this message and exit.                                                    │ 
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

This will create a refactoring file from a template.

<h3>Init Command Usage</h3>

* **Without flags** : Will check-out to a new branch and a template refactoring file.
* **Package and Version flags** can only be used together. They will be used to format the refactoring file name
  and the new branch name.
* **Registry flag** is the directory that holds the refactoring files. Registries can also be a link to a git repository that holds the refactoring files.
* **Git flag** : Activates or deactivates git functionalities.

<h3>Refactoring API</h3>

The template refactoring file will look like something like this.
For the current version, these are the supported transformations.
If you encounter a refactoring that is not supported, you have the option to utilize the `apply_custom_transformation()`
method, which accepts a LibCST `CSTTransformer`.

```python
from syncupgrade import SyncUpgrade, RenameRefactoring, AddRefactoring


def update():
  renamer = (
    RenameRefactoring()
    .rename_param("old_param_name", 'new_param_name')
    .rename_imports("old_import_attribute", "new_import_attribute")
    .rename_class("old_class_name", "new_class_name")
    .rename_variables("old_variable_name", "new_variable_name")
    .rename_functions("old_function_name", "new_function_name")
  )
  add = (
    AddRefactoring()
    .add_import_attribute("ImportAlias", "new_import_attribute")
  )

  return (
    SyncUpgrade()
    .apply_renames(renamer)
    .apply_add(add)
    .apply_custom_transformation()
  )
```

Once you define your changes, you can now apply them.

```console
refactor apply --help

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --package                    TEXT                          Package to upgrade                                                            │
│ --version                    TEXT                          New package version                                                           │
│ --base-branch                TEXT                          Git branch to merge to                                                        │
│ --apply-mode                 [dry_run|apply|pull_request]  Check, apply changes or create a pull request [default: dry_run]              │
│ --registry                   TEXT                          Directory where refactoring files are saved [default: ./refactoring_files/]   │
│ --git            --no-git                                  Activate git [default: git]                                                   │
│ --help                                                     Show this message and exit.                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

<h3>Apply Command Usage</h3>

This will fetch the defined changes from the refactoring file under registry and subsequently applying those changes.

* **Without flags** : Will first examine the current branch and, if needed, switch to a new branch. Next, it will fetch
  all refactoring files located in the registry directory and perform a dry run, describing the changes without actually
  applying them.
* **Package and Version flags** if used, will only fetch a specific refactoring file.
* **Registry flag** is the directory that holds the refactoring files. Registries can also be a link to a git repository that holds the refactoring files.
* **Git flag** : Activates or deactivates git functionalities.
* **Apply Mode flag** The methods to apply the code changes. A `Dry Run` will display the differences without actually
  modifying the code. `Apply` will locally apply the changes to the codebase. `Pull Request` will both apply the changes
  and create a pull request for further review and integration.
* **Base Branch flag** The destination merge branch. Will only be used for pull request creation. If not specified, the
  repository main branch will be fetched and used as base branch.

:warning: **Always run a dry run before an apply or a pull request**

# Contributing
Contributions are always welcomed whether it's a bug fix, new feature, documentation improvement, or any other valuable input.

If you find a bug, have a feature request, or encounter any issues while using the project, please submit an issue in our [Issue Tracker](https://github.com/datamindedbe/sync-upgrade/issues/new).
Make sure to include as many details as possible, such as the steps to reproduce the problem, relevant environment information, and the expected outcome.

To make a contribution, please follow these steps.
1. Clone this reposotory and create a new branch.
2. Make your contributions.
3. Add or updates tests, if necessary.
4. Open a Pull Request with a comprehensive description of changes.

