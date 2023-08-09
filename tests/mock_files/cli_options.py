class CliOptions:
    dry_run_no_git_options = ["apply", "--no-git", "--registry", "tests/conftest.py"]
    apply_pull_request_no_git_fail_options = ["apply", "--no-git", "--registry", "tests/conftest.py", "--apply-mode",
                                              "pull_request"]
    apply_no_git_options = ["apply", "--no-git", "--registry", "tests/conftest.py", "--apply-mode", "apply"]
    apply_missing_version_no_git_options = ["apply", "--no-git", "--registry", "tests/conftest.py", "--package",
                                            "package_name"]
    apply_wrong_package_no_git_options = ["apply", "--no-git", "--registry", "tests/conftest.py", "--package",
                                          "package_name1", "--version", "2"]

    dry_run_wrong_registry_no_git_options = ["apply", "--no-git", "--registry", "wrong_file.py"]
    dry_run_no_update_no_git_options = ["apply", "--no-git", "--registry", "tests/mock_files/mock_code.py"]
    init_no_git_options = ["init", "--no-git", "--registry", "tests/mock_registry"]
    init_package_version_no_git_options = ["init", "--no-git", "--registry", "tests/mock_registry", "--package",
                                           "package", "--version", "2"]
    init_no_git_exists_options = ["init", "--no-git", "--registry", "tests/mock_registry"]